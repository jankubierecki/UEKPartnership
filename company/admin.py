from django.contrib import admin
from django.utils.html import format_html

from common.admin import ReadOnlyModelAdmin
from company.models import CompanyToCompanyContactPerson, Company, CompanyContactPerson, EmailInformedUsers
from university.views import CompanyContactPersonAutocomplete


class CompanyToCompanyContactPersonInlineAdmin(admin.TabularInline):
    model = CompanyToCompanyContactPerson
    extra = 0
    min_num = 1
    verbose_name_plural = "Przypisane osoby do kontaktu"
    verbose_name = " osoby"
    fields = ['company_contact_person', 'created_at']
    readonly_fields = ['created_at']
    autocomplete_fields = ["company_contact_person"]


class CompanyContactPersonToCompanyInlineAdmin(CompanyToCompanyContactPersonInlineAdmin):
    extra = 0
    min_num = 0
    fields = ['company', 'created_at']
    verbose_name_plural = "Przypisane Firmy"
    verbose_name = " - przypisz tej osobie kolejną firmę"
    autocomplete_fields = ["company"]


@admin.register(Company)
class CompanyAdmin(ReadOnlyModelAdmin, admin.ModelAdmin):
    change_form_template = "admin/company_change_form.html"
    change_list_template = "admin/company_change_list.html"
    list_display = ["name", "city", "street", "zip_code", "phone", "email", "industry", "get_website_url",
                    "created_at", "updated_at"]
    search_fields = ["name", "city", "zip_code", "industry", "company_contact_persons__first_name",
                     "company_contact_persons__last_name"]
    list_filter = ["created_at", "updated_at", "city", "industry"]

    fieldsets = (
        ("Informacje podstawowe", {'fields': ['name', 'phone', 'website', 'email']}),
        ("Dane do kontaktu", {'fields': [('city', 'street', 'zip_code')]}),
        ("O Firmie",
         {'fields': ['industry', 'krs_code', 'nip_code', 'created_at', 'updated_at', 'additional_info',
                     'privacy_email_date_send']})

    )
    readonly_fields = ["created_at", "updated_at", 'privacy_email_date_send']
    inlines = [CompanyToCompanyContactPersonInlineAdmin]

    class Media:
        css = {
            'all': ('university/css/company_display.css',)
        }

    def get_website_url(self, obj: Company):
        return format_html('<a href="%s">%s' % (obj.website, obj.website))

    def get_email_url(self, obj: Company):
        return format_html('<a href="%s">%s' % (obj.id, obj.email))

    get_website_url.short_description = 'Strona Internetowa'

    def get_queryset(self, request):
        return Company.objects.prefetch_related("partnerships").all()


@admin.register(CompanyContactPerson)
class CompanyContactPersonAdmin(ReadOnlyModelAdmin, admin.ModelAdmin):
    list_display = ["first_name", "get_last_name_url", "phone", "get_email_url"]
    fields = ["first_name", "last_name", "phone", "email", "created_at", "updated_at", 'privacy_email_date_send']
    list_filter = ["created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at", 'privacy_email_date_send']
    search_fields = ["first_name", "last_name", "phone", "company__name"]
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


@admin.register(EmailInformedUsers)
class EmailInformedUsersAdmin(admin.ModelAdmin):
    list_display = ["email", "created_at"]
    list_filter = ["created_at"]
    readonly_fields = list_display
    search_fields = list_display

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
