from django.contrib import admin

from .models import User, Address, Privilege


class AddressInline(admin.StackedInline):
    model = Address
    extra = 0


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['email', 'username', 'is_registered', 'date_registered', 'privilege']}),
        ('Personal information', {'fields': ['first_name', 'last_name', 'phone', ]}),
        ('Account information', {'fields': ['password', 'last_login', 'date_joined', 'is_active', 'is_staff', ]}),
    ]
    inlines = [AddressInline]
    list_display = ('email', 'username', 'is_registered', 'privilege', )
    list_filter = ['date_joined']
    search_fields = ['email']


admin.site.register(User, UserAdmin)
admin.site.register(Address)
admin.site.register(Privilege)