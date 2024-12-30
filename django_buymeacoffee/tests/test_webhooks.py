from django.test import TestCase
from django.urls import reverse
from ..models import Supporter, Donation, Extra, Membership
import json
from datetime import datetime


class WebhookTestCase(TestCase):
    def setUp(self):
        self.webhook_url = '/api/buymeacoffee/webhook'  # Update this based on your URL configuration
        self.maxDiff = None

    def test_donation_created(self):
        payload = {
            "type": "donation.created",
            "live_mode": False,
            "attempt": 1,
            "created": 1732347758,
            "event_id": 1,
            "data": {
                "id": 58,
                "amount": 5,
                "object": "payment",
                "status": "succeeded",
                "message": "John bought you a coffee",
                "currency": "USD",
                "refunded": "false",
                "created_at": 1676544557,
                "note_hidden": "true",
                "refunded_at": None,
                "support_note": "Thanks for the good work",
                "support_type": "Supporter",
                "supporter_name": "John",
                "supporter_id": 2345,
                "supporter_email": "john@example.com",
                "transaction_id": "pi_3Mc51bJEtINljGAa0zVykgUE",
                "application_fee": "0.25",
                "total_amount_charged": "5.45"
            }
        }

        response = self.client.post(
            self.webhook_url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "success",
            "message": "Processed donation.created event"
        })

        # Check database records
        supporter = Supporter.objects.get(id=2345)
        self.assertEqual(supporter.name, "John")
        self.assertEqual(supporter.email, "john@example.com")

        donation = Donation.objects.get(id=58)
        self.assertEqual(donation.supporter, supporter)
        self.assertEqual(float(donation.amount), 5.0)
        self.assertEqual(donation.currency, "USD")
        self.assertEqual(donation.status, "succeeded")
        self.assertEqual(donation.support_type, "Supporter")
        self.assertFalse(donation.refunded)

    def test_extra_purchase_created(self):
        payload = {
            "type": "extra_purchase.created",
            "live_mode": False,
            "attempt": 1,
            "created": 1732347901,
            "event_id": 1,
            "data": {
                "id": 59,
                "amount": 75,
                "extras": [
                    {
                        "id": 3,
                        "title": "Content Creation Advice",
                        "amount": "75.00",
                        "quantity": 2,
                        "currency": "USD",
                        "description": "Hop on a Zoom call with me",
                        "extra_question": "Would you like me to prepare?",
                        "question_answers": []
                    }
                ],
                "status": "succeeded",
                "currency": "USD",
                "refunded": "false",
                "created_at": 1676545577,
                "supporter_name": "John",
                "supporter_id": 2345,
                "supporter_email": "john@example.com",
                "transaction_id": "pi_3Mc5I3JEtINljGAa0XZxB3XG",
                "application_fee": "3.75",
                "total_amount_charged": "77.48"
            }
        }

        response = self.client.post(
            self.webhook_url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "success",
            "message": "Processed extra_purchase.created event"
        })

        # Check database records
        donation = Donation.objects.get(id=59)
        self.assertEqual(donation.support_type, "Extra")
        self.assertEqual(float(donation.amount), 75.0)

        extra = Extra.objects.get(id=3)
        self.assertEqual(extra.donation, donation)
        self.assertEqual(extra.title, "Content Creation Advice")
        self.assertEqual(float(extra.amount), 75.00)
        self.assertEqual(extra.quantity, 2)

    def test_membership_started(self):
        payload = {
            "type": "membership.started",
            "live_mode": False,
            "attempt": 1,
            "created": 1732347922,
            "event_id": 1,
            "data": {
                "id": 16,
                "amount": 1,
                "status": "active",
                "currency": "USD",
                "paused": "false",
                "canceled": "false",
                "psp_id": "sub_1Mc70vJEtINljGAa1xaGI5q9",
                "duration_type": "month",
                "membership_level_id": 5,
                "membership_level_name": "Basic",
                "started_at": 1676552204,
                "supporter_name": "John",
                "supporter_id": 2345,
                "supporter_email": "john@example.com",
                "current_period_end": 1678971401,
                "current_period_start": 1676552201
            }
        }

        response = self.client.post(
            self.webhook_url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "success",
            "message": "Processed membership.started event"
        })

        # Check database records
        membership = Membership.objects.get(id=16)
        self.assertEqual(membership.status, "active")
        self.assertEqual(membership.duration_type, "month")
        self.assertEqual(membership.membership_level_name, "Basic")
        self.assertFalse(membership.paused)
        self.assertFalse(membership.canceled)

    def test_membership_cancelled(self):
        # First create an active membership
        self.test_membership_started()

        payload = {
            "type": "membership.cancelled",
            "live_mode": False,
            "attempt": 1,
            "created": 1732347968,
            "event_id": 1,
            "data": {
                "id": 16,
                "amount": 1,
                "status": "canceled",
                "currency": "USD",
                "paused": "false",
                "canceled": "true",
                "psp_id": "sub_1Mc70vJEtINljGAa1xaGI5q9",
                "duration_type": "month",
                "membership_level_id": 5,
                "membership_level_name": "Basic",
                "started_at": 1676552204,
                "canceled_at": 1676552379,
                "supporter_name": "John",
                "supporter_id": 2345,
                "supporter_email": "john@example.com",
                "current_period_end": 1678971401,
                "current_period_start": 1676552201,
                "supporter_feedback": "CANCELLED_BY_CREATOR"
            }
        }

        response = self.client.post(
            self.webhook_url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "success",
            "message": "Processed membership.cancelled event"
        })

        # Check database records
        membership = Membership.objects.get(id=16)
        self.assertEqual(membership.status, "canceled")
        self.assertTrue(membership.canceled)
        self.assertEqual(membership.supporter_feedback, "CANCELLED_BY_CREATOR")
        self.assertIsNotNone(membership.canceled_at)
