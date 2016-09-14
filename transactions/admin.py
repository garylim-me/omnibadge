from django.contrib import admin

from .models import Transaction, DocumentType


# class DocumentTypeInline(admin.StackedInline):
class DocumentTypeInline(admin.TabularInline):
    model = Transaction.document_type.through
    extra = 0


class TransactionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['company', ]}),
        ('Request information', {'fields': ['ui_type', 'user', 'service', 'document_type', ]}),
        ('Technical information', {'fields': ['transaction_token', 'js_result', 'version', ]}),
        ('Logged information',
         {'fields': ['date_created', 'date_completed', 'user_ip', 'company_ip', ]}),
    ]
    inlines = [DocumentTypeInline]
    list_display = ('company', 'user', 'service', 'date_created', )
    list_filter = ['date_created']
    search_fields = ['user']


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(DocumentType)