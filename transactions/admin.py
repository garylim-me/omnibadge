from django.contrib import admin

from .models import Transaction, DocumentType, TransactionToken
from documents.models import UserDocument


class DocumentsInline(admin.TabularInline):
    model = UserDocument


class TransactionAdmin(admin.ModelAdmin):

    def user_document_list(self, transaction):
        user_documents = []
        for user_document in transaction.user_documents.all():
            user_documents.append(str(user_document.id))
        return ' '.join(user_documents)

        user_document_list.short_description = 'Documents'

    fieldsets = [
        (None, {'fields': ['company', ]}),
        ('Request information', {'fields': ['ui_type', 'user', 'document_type', ]}),  # temp removal TODO: 'service',
        ('Technical information', {'fields': ['transaction_token', 'js_result', 'version', ]}),
        ('Logged information',
         {'fields': ['date_created', 'date_completed', 'user_ip', 'company_ip', 'user_documents']}),
    ]
    # inlines = [
    #     DocumentsInline,
    # ]
    list_display = ('id', 'company', 'user', 'date_created', 'user_document_list')  # temp removal TODO: 'service',
    list_filter = ['date_created']
    search_fields = ['user']


class TransactionTokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'transaction', 'created', )
    list_filter = ['created']
    search_fields = ['transaction']

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(DocumentType)
admin.site.register(TransactionToken, TransactionTokenAdmin)
