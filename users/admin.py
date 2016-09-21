from django.contrib import admin

from .models import User, Privilege, SessionToken
from common import models as common_models

from rest_framework.authtoken.admin import TokenAdmin

# registering token fields into admin
TokenAdmin.raw_id_fields = ('user',)


class AddressInline(admin.StackedInline):
    model = common_models.Address
    extra = 0


class UserAdmin(admin.ModelAdmin):
    # No point adding password field -- meaningless?
    fieldsets = [
        (None, {'fields': ['email', 'username', 'is_registered', 'date_registered', ]}),
        ('Business information', {'fields': ['privilege', 'company', ]}),
        ('Personal information', {'fields': ['first_name', 'last_name', 'phone', ]}),
        ('Account information', {'fields': ['password', 'last_login', 'date_joined', 'is_active', 'is_staff', ]}),
    ]
    inlines = [AddressInline]
    list_display = ('email', 'username', 'is_registered', 'privilege', )
    list_filter = ['date_joined']
    search_fields = ['email']

admin.site.register(User, UserAdmin)


class PrivilegeAdmin(admin.ModelAdmin):
    # No point adding password field -- meaningless?
    fieldsets = [
        (None, {'fields': ['name', ]}),
        ('Personal', {'fields': ['user_read',
                                 'user_write',
                                 'user_verify',
                                 'user_delete', ]}),
        ('Business: Transaction Access', {'fields': ['company_read_transactions',
                                                     'company_write_transactions',
                                                     'company_verify_transactions',
                                                     'company_delete_transactions', ]}),
        ('Business: Document Access', {'fields': ['company_read_documents',
                                                  'company_write_documents',
                                                  'company_verify_documents',
                                                  'company_delete_documents', ]}),
        ('Admin', {'fields': ['all_read',
                              'all_verify',
                              'all_write',
                              'all_delete', ]}),
    ]
    list_display = ('name', 'user_read', 'company_read_transactions', 'company_read_documents', 'all_read', )

admin.site.register(Privilege, PrivilegeAdmin)


class SessionTokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'privilege', 'created', )
    list_filter = ['created']
    search_fields = ['user']

admin.site.register(SessionToken, SessionTokenAdmin)
