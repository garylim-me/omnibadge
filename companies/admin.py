from django.contrib import admin

from .models import Company

from services import models as service_models


# class DocumentTypeInline(admin.StackedInline):
class ServiceSubscriptionTypeInline(admin.TabularInline):
    model = service_models.ServiceSubscription
    extra = 1


class CompanyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'white_label', 'date_registered', 'is_active']}),
    ]
    inlines = [ServiceSubscriptionTypeInline]
    list_display = ('name', 'white_label', 'date_registered', 'is_active')
    list_filter = ['date_registered']
    search_fields = ['name']


admin.site.register(Company, CompanyAdmin)
