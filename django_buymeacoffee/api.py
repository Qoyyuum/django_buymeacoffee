from django.shortcuts import get_object_or_404
from django_ninja import NinjaAPI, Schema
from typing import List, Optional
from datetime import datetime
from django.conf import settings
from .models import Supporter, Donation, Extra, Membership

api = NinjaAPI(urls_namespace='buymeacoffee')


class WebhookSchema(Schema):
    type: str
    live_mode: bool
    attempt: int
    created: int
    event_id: int
    data: dict


def handle_donation_event(event_type: str, data: dict, supporter: Supporter):
    """Handle donation.created and donation.refunded events"""
    if event_type == 'donation.created':
        donation = Donation.objects.create(
            id=data['id'],
            supporter=supporter,
            amount=data['amount'],
            message=data.get('message'),
            support_note=data.get('support_note'),
            currency=data['currency'],
            transaction_id=data['transaction_id'],
            support_type='Supporter',
            status=data['status'],
            created_at=datetime.fromtimestamp(data['created_at']),
            note_hidden=data.get('note_hidden', False),
            application_fee=data['application_fee'],
            total_amount_charged=data['total_amount_charged']
        )
        return donation
    elif event_type == 'donation.refunded':
        donation = get_object_or_404(Donation, id=data['id'])
        donation.refunded = True
        donation.refunded_at = datetime.fromtimestamp(data['refunded_at'])
        donation.status = 'refunded'
        donation.save()
        return donation


def handle_extra_purchase_event(event_type: str, data: dict, supporter: Supporter):
    """Handle extra_purchase.created and extra_purchase.refunded events"""
    if event_type == 'extra_purchase.created':
        donation = Donation.objects.create(
            id=data['id'],
            supporter=supporter,
            amount=data['amount'],
            message=data.get('message'),
            support_note=data.get('support_note'),
            currency=data['currency'],
            transaction_id=data['transaction_id'],
            support_type='Extra',
            status=data['status'],
            created_at=datetime.fromtimestamp(data['created_at']),
            note_hidden=data.get('note_hidden', False),
            application_fee=data['application_fee'],
            total_amount_charged=data['total_amount_charged']
        )
        
        # Create Extra objects for each extra in the purchase
        for extra_data in data['extras']:
            Extra.objects.create(
                id=extra_data['id'],
                donation=donation,
                title=extra_data['title'],
                amount=extra_data['amount'],
                quantity=extra_data['quantity'],
                currency=extra_data['currency'],
                description=extra_data['description'],
                extra_question=extra_data.get('extra_question'),
                question_answers=extra_data.get('question_answers', [])
            )
        return donation
    elif event_type == 'extra_purchase.refunded':
        donation = get_object_or_404(Donation, id=data['id'])
        donation.refunded = True
        donation.refunded_at = datetime.fromtimestamp(data['refunded_at'])
        donation.status = 'refunded'
        donation.save()
        return donation


def handle_membership_event(event_type: str, data: dict, supporter: Supporter):
    """Handle membership.started, membership.cancelled, and membership.updated events"""
    if event_type == 'membership.started':
        membership = Membership.objects.create(
            id=data['id'],
            supporter=supporter,
            amount=data['amount'],
            currency=data['currency'],
            psp_id=data['psp_id'],
            duration_type=data['duration_type'],
            membership_level_id=data['membership_level_id'],
            membership_level_name=data['membership_level_name'],
            status=data['status'],
            paused=data['paused'] == 'true',
            canceled=data['canceled'] == 'true',
            started_at=datetime.fromtimestamp(data['started_at']),
            canceled_at=datetime.fromtimestamp(data['canceled_at']) if data.get('canceled_at') else None,
            current_period_start=datetime.fromtimestamp(data['current_period_start']),
            current_period_end=datetime.fromtimestamp(data['current_period_end']),
            note_hidden=data.get('note_hidden', False),
            support_note=data.get('support_note')
        )
        return membership
    elif event_type in ['membership.cancelled', 'membership.updated']:
        membership = get_object_or_404(Membership, id=data['id'])
        membership.status = data['status']
        membership.paused = data['paused'] == 'true'
        membership.canceled = data['canceled'] == 'true'
        membership.canceled_at = datetime.fromtimestamp(data['canceled_at']) if data.get('canceled_at') else None
        membership.current_period_start = datetime.fromtimestamp(data['current_period_start'])
        membership.current_period_end = datetime.fromtimestamp(data['current_period_end'])
        membership.supporter_feedback = data.get('supporter_feedback')
        membership.save()
        return membership


@api.post("/webhook")
def handle_webhook(request, payload: WebhookSchema):
    """Handle incoming webhooks from Buy Me a Coffee"""
    event_type = payload.type
    data = payload.data
    
    # Get or create supporter
    supporter_data = {
        'id': data['supporter_id'],
        'name': data['supporter_name'],
        'email': data['supporter_email'],
    }
    supporter, _ = Supporter.objects.get_or_create(
        id=supporter_data['id'],
        defaults=supporter_data
    )
    
    # Handle different event types
    if event_type.startswith('donation'):
        result = handle_donation_event(event_type, data, supporter)
    elif event_type.startswith('extra_purchase'):
        result = handle_extra_purchase_event(event_type, data, supporter)
    elif event_type.startswith('membership'):
        result = handle_membership_event(event_type, data, supporter)
    else:
        return {"status": "error", "message": f"Unknown event type: {event_type}"}
        
    return {"status": "success", "message": f"Processed {event_type} event"}
