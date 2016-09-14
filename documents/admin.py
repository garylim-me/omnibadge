from django.contrib import admin

from .models import DocPassport, DocForm


class DocPassportAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['date_created', 'version', 'document_type', 'user', 'transaction']}),
        ('User input', {'fields': ['document_image', 'document_filename', 'document_filename2', ]}),
        ('Parsed data', {'fields': ['parsed_passport_id', 'parsed_first_name', 'parsed_last_name',
                                    'parsed_nationality', 'parsed_dob', 'parsed_issue_date', 'parsed_expiry_date', ]}),
        ('verification', {'fields': ['verified', 'date_verified', ]}),
    ]
    # inlines = [DocumentTypeInline]
    list_display = ('document_type', 'user', 'transaction')
    list_filter = ['date_created']
    search_fields = ['user']

admin.site.register(DocPassport, DocPassportAdmin)
admin.site.register(DocForm)
