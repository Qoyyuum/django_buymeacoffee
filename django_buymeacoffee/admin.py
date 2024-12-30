from django.contrib import admin
from .models import Supporter, Donation, Extra, Membership


@admin.register(Supporter)
class SupporterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)
    readonly_fields = ('id', 'created_at')


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('supporter', 'amount', 'currency', 'support_type', 'status', 'created_at')
    list_filter = ('support_type', 'status', 'refunded', 'currency', 'created_at')
    search_fields = ('supporter__name', 'supporter__email', 'transaction_id')
    readonly_fields = ('id', 'created_at')
    raw_id_fields = ('supporter',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('supporter')


@admin.register(Extra)
class ExtraAdmin(admin.ModelAdmin):
    list_display = ('title', 'donation', 'amount', 'currency', 'quantity')
    list_filter = ('currency',)
    search_fields = ('title', 'donation__supporter__name', 'donation__supporter__email')
    raw_id_fields = ('donation',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('donation', 'donation__supporter')


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('supporter', 'membership_level_name', 'amount', 'currency', 'status', 'duration_type')
    list_filter = ('status', 'duration_type', 'currency', 'paused', 'canceled')
    search_fields = ('supporter__name', 'supporter__email', 'psp_id', 'membership_level_name')
    readonly_fields = ('id', 'started_at', 'current_period_start', 'current_period_end')
    raw_id_fields = ('supporter',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('supporter')
