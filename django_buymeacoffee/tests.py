from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from .models import Supporter, Donation, Extra, Membership

class WebhookTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('buymeacoffee:webhook')
        self.supporter_data = {
            'id': 1,
            'name': 'Test Supporter',
            'email': 'supporter@example.com'
        }
        self.supporter = Supporter.objects.create(**self.supporter_data)

    def test_handle_donation_created(self):
        payload = {
            'type': 'donation.created',
            'live_mode': True,
            'attempt': 1,
            'created': int(timezone.now().timestamp()),
            'event_id': 1,
            'data': {
                'id': 1,
                'supporter_id': self.supporter.id,
                'amount': 500,
                'currency': 'USD',
                'transaction_id': 'txn_123',
                'status': 'completed',
                'created_at': int(timezone.now().timestamp()),
                'application_fee': 50,
                'total_amount_charged': 550
            }
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Donation.objects.count(), 1)

    def test_handle_extra_purchase_created(self):
        payload = {
            'type': 'extra_purchase.created',
            'live_mode': True,
            'attempt': 1,
            'created': int(timezone.now().timestamp()),
            'event_id': 1,
            'data': {
                'id': 2,
                'supporter_id': self.supporter.id,
                'amount': 1000,
                'currency': 'USD',
                'transaction_id': 'txn_456',
                'status': 'completed',
                'created_at': int(timezone.now().timestamp()),
                'application_fee': 100,
                'total_amount_charged': 1100,
                'extras': [
                    {
                        'id': 1,
                        'title': 'Extra 1',
                        'amount': 500,
                        'quantity': 2,
                        'currency': 'USD',
                        'description': 'Description for Extra 1'
                    }
                ]
            }
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Donation.objects.count(), 1)
        self.assertEqual(Extra.objects.count(), 1)

    def test_handle_membership_started(self):
        payload = {
            'type': 'membership.started',
            'live_mode': True,
            'attempt': 1,
            'created': int(timezone.now().timestamp()),
            'event_id': 1,
            'data': {
                'id': 3,
                'supporter_id': self.supporter.id,
                'amount': 1500,
                'currency': 'USD',
                'psp_id': 'psp_789',
                'duration_type': 'monthly',
                'membership_level_id': 1,
                'membership_level_name': 'Gold',
                'status': 'active',
                'paused': 'false',
                'canceled': 'false',
                'started_at': int(timezone.now().timestamp()),
                'current_period_start': int(timezone.now().timestamp()),
                'current_period_end': int(timezone.now().timestamp()) + 2592000
            }
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Membership.objects.count(), 1)
