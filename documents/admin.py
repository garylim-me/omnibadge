from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import DocPassport, DocForm, UserDocument


# not optimal to view/add
class UserDocumentInline(GenericTabularInline):
    ct_field = "document_type"
    ct_fk_field = "document_id"
    model = UserDocument
    extra = 0


class DocPassportAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['date_created', 'version', 'document_type', 'owner', 'transaction', ]}),
        ('User input', {'fields': ['document_image', 'document_filename', 'document_filename2', ]}),
        ('Parsed data', {'fields': ['parsed_passport_id', 'parsed_first_name', 'parsed_last_name',
                                    'parsed_nationality', 'parsed_dob', 'parsed_issue_date', 'parsed_expiry_date', ]}),
        ('verification', {'fields': ['verified', 'date_verified', ]}),
    ]
    inlines = [UserDocumentInline]
    list_display = ('document_type', 'owner', 'transaction')
    list_filter = ['date_created']
    search_fields = ['owner']


# class UserDocumentAdmin(admin.ModelAdmin):
#     # define the related_lookup_fields
#     related_lookup_fields = {
#         'generic': [['document_type', 'document_id'], ],
#     }


admin.site.register(DocPassport, DocPassportAdmin)
admin.site.register(DocForm)
admin.site.register(UserDocument)
# admin.site.register(UserDocument, UserDocumentAdmin)



