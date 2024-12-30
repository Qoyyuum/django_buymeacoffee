from django.db import models
from django.utils import timezone


class Supporter(models.Model):
    id = models.BigIntegerField(primary_key=True)  # supporter_id from BMAC
    name = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        verbose_name = 'Supporter'
        verbose_name_plural = 'Supporters'


class Donation(models.Model):
    SUPPORT_TYPES = [
        ('Supporter', 'One-time Support'),
        ('Extra', 'Extra Purchase'),
    ]
    
    id = models.BigIntegerField(primary_key=True)  # BMAC payment id
    supporter = models.ForeignKey(Supporter, on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True, null=True)
    support_note = models.TextField(blank=True, null=True)
    currency = models.CharField(max_length=3)
    transaction_id = models.CharField(max_length=255)
    support_type = models.CharField(max_length=20, choices=SUPPORT_TYPES)
    status = models.CharField(max_length=20)
    refunded = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    refunded_at = models.DateTimeField(null=True, blank=True)
    note_hidden = models.BooleanField(default=False)
    application_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount_charged = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'

    def __str__(self):
        return f"{self.supporter.name} - {self.amount} {self.currency} ({self.created_at.date()})"


class Extra(models.Model):
    id = models.BigIntegerField(primary_key=True)
    donation = models.ForeignKey(Donation, related_name='extras', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    currency = models.CharField(max_length=3)
    description = models.TextField()
    extra_question = models.TextField(blank=True, null=True)
    question_answers = models.JSONField(default=list)

    class Meta:
        verbose_name = 'Extra'
        verbose_name_plural = 'Extras'

    def __str__(self):
        return f"{self.title} - {self.amount} {self.currency}"


class Membership(models.Model):
    DURATION_TYPES = [
        ('month', 'Monthly'),
        ('year', 'Yearly'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('paused', 'Paused'),
    ]
    
    id = models.BigIntegerField(primary_key=True)
    supporter = models.ForeignKey(Supporter, on_delete=models.CASCADE, related_name='memberships')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    psp_id = models.CharField(max_length=255)  # Payment Service Provider ID
    duration_type = models.CharField(max_length=10, choices=DURATION_TYPES)
    membership_level_id = models.IntegerField()
    membership_level_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    paused = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    started_at = models.DateTimeField()
    canceled_at = models.DateTimeField(null=True, blank=True)
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    supporter_feedback = models.TextField(null=True, blank=True)
    note_hidden = models.BooleanField(default=False)
    support_note = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Membership'
        verbose_name_plural = 'Memberships'

    def __str__(self):
        return f"{self.supporter.name} - {self.membership_level_name} ({self.status})"
