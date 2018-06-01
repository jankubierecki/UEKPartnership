from django.contrib import admin
from django.utils.html import format_html

from common.admin import ReadOnlyModelAdmin
from company.models import CompanyToCompanyContactPerson, Company, CompanyContactPerson
from university.views import CompanyContactPersonAutocomplete


class CompanyToCompanyContactPersonInlineAdmin(admin.TabularInline):
    model = CompanyToCompanyContactPerson
    extra = 0
    verbose_name_plural = "Przypisane osoby do kontaktu"
    fields = ['company_contact_person', 'created_at']
    readonly_fields = ['created_at']
    autocomplete_fields = ["company_contact_person"]


class CompanyContactPersonToCompanyInlineAdmin(CompanyToCompanyContactPersonInlineAdmin):
    fields = ['company', 'created_at']
    verbose_name_plural = "Przypisane Firmy"
    autocomplete_fields = ["company"]


@admin.register(Company)
class CompanyAdmin(ReadOnlyModelAdmin, admin.ModelAdmin):
    list_display = ["name", "city", "street", "zip_code", "phone", "industry", "krs_code", "website", "created_at",
                    "updated_at"]
    search_fields = ["name", "city", "zip_code", "industry", "company_contact_persons__first_name",
                     "company_contact_persons__last_name"]
    list_filter = ["created_at", "updated_at"]
    fieldsets = (
        ("Informacje podstawowe", {'fields': ['name', 'phone', 'website']}),
        ("Dane do kontaktu", {'fields': [('city', 'street', 'zip_code')]}),
        ("O Firmie", {'fields': ['industry', 'krs_code', 'created_at', 'updated_at']})

    )
    readonly_fields = ["created_at", "updated_at"]
    inlines = [CompanyToCompanyContactPersonInlineAdmin]


@admin.register(CompanyContactPerson)
class CompanyContactPersonAdmin(ReadOnlyModelAdmin, admin.ModelAdmin):
    list_display = ["first_name", "get_last_name_url", "phone", "get_email_url"]
    fields = ["first_name", "last_name", "phone", "email", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]
    search_fields = ["first_name", "last_name", "phone", "companies__name"]
    inlines = [CompanyContactPersonToCompanyInlineAdmin]

    def get_email_url(self, obj: CompanyContactPerson):
        return format_html('<a href="%s">%s' % (obj.id, obj.email))

    def get_last_name_url(self, obj: CompanyContactPerson):
        return format_html('<a href="%s">%s' % (obj.id, obj.last_name))

    def autocomplete_view(self, request):
        return CompanyContactPersonAutocomplete.as_view(model_admin=self)(request)

    get_email_url.allow_tags = True
    get_email_url.short_description = 'Email'
    get_last_name_url.short_description = 'Nazwisko'
