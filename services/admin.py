from django.contrib import admin

from .models import Service


class ServiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Basic features', {'fields': ['verify_passport', 'verify_govt_id', ]}),
        ('Standard verification features', {'fields': ['live_image', 'verify_nric_ica', 'verify_billing_address',
                                                       'verify_mobile_number', ]}),
        ('User management features', {'fields': ['track_expiry', 'follow_up_request', 'network_sharing', ]}),
        ('Premium verification features', {'fields': ['fast_verification', 'phone_interviews', ]}),
    ]
    list_display = ('name', )


admin.site.register(Service, ServiceAdmin)
