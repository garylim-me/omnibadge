from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import DocPassport, DocForm, UserDocument
from transactions.models import Transaction


# not optimal to view/add
class UserDocumentInline(GenericTabularInline):
    ct_field = "document_type"
    ct_fk_field = "document_id"
    model = UserDocument
    extra = 0


# class TransactionInline(admin.StackedInline):
#     model = Transaction
#     extra = 0


class UserDocumentAdmin(admin.ModelAdmin):

    def transactions_list(self, obj):
        return ",".join([str(transaction.id) for transaction in obj.transactions.all()])
    transactions_list.short_description = 'Transactions'

    # def all_transactions(self, obj):
    #     return obj.transactions.all()
    # all_transactions.short_description = 'Transaction objects'

    fieldsets = [
        (None, {'fields': ['date_created', 'version', 'user', ]}),
        ('linked document', {'fields': ['document_type', 'document_id', ]}),
        ('verification', {'fields': ['verified', 'date_verified', ]}),
    ]
    # Used by grappelli:
    # related_lookup_fields = {
    #             'generic': [['document_type', 'document_id'], ],
    # }
    # inlines = [
    #     TransactionInline,
    # ]
    list_display = ('id', 'document_type', 'user', 'transactions_list')
    list_filter = ['date_created']
    search_fields = ['user']


class DocPassportAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User input', {'fields': ['document_image', 'document_filename', 'document_filename2', ]}),
        ('Parsed data', {'fields': ['parsed_passport_id', 'parsed_first_name', 'parsed_last_name',
                                    'parsed_nationality', 'parsed_dob', 'parsed_issue_date', 'parsed_expiry_date', ]}),
    ]
    inlines = [UserDocumentInline]


# class UserDocumentAdmin(admin.ModelAdmin):
#     # define the related_lookup_fields
#     related_lookup_fields = {
#         'generic': [['document_type', 'document_id'], ],
#     }


admin.site.register(DocPassport, DocPassportAdmin)
admin.site.register(DocForm)
admin.site.register(UserDocument, UserDocumentAdmin)
# admin.site.register(UserDocument, UserDocumentAdmin)



