from django.contrib import admin
from django.utils.html import format_html
from django import forms

from common.admin import ReadOnlyModelAdmin
from university.models import InstituteUnit, UniversityContactPerson, \
    InstituteUnitToUniversityContactPerson
from university.views import UniversityContactPersonAutocomplete


class InstituteUnitToUniversityContactPersonInlineAdmin(ReadOnlyModelAdmin, admin.TabularInline):
    model = InstituteUnitToUniversityContactPerson
    extra = 0
    min_num = 1
    verbose_name_plural = "przypisane osoby"
    verbose_name = " osoby"
    fields = ['university_contact_person', 'created_at']
    readonly_fields = ['created_at']
    autocomplete_fields = ["university_contact_person"]


# TODO clean view on delete contact persons


class UniversityContactPersonToInstituteUnitInlineAdmin(InstituteUnitToUniversityContactPersonInlineAdmin):
    extra = 0
    min_num = 0
    fields = ['institute_unit', 'created_at']
    verbose_name_plural = "Przypisane jednostki współpracujące UEK"
    verbose_name = "Przypisz tej osobie kolejną jednostkę UEK"
    autocomplete_fields = ['institute_unit']


@admin.register(InstituteUnit)
class InstituteUnitAdmin(ReadOnlyModelAdmin, admin.ModelAdmin):
    change_form_template = "admin/institute_unit_change_form.html"
    change_list_template = "admin/institute_unit_change_list.html"

    list_display = ["name", "created_at", "updated_at"]
    search_fields = ["name"]
    list_filter = ["created_at", "updated_at"]
    fields = ["name", "additional_info", "created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]
    filter_horizontal = ['university_contact_persons']
    inlines = [InstituteUnitToUniversityContactPersonInlineAdmin]

    class Media:
        css = {
            'all': ('university/css/institute_unit_display.css',)
        }

    def get_queryset(self, request):
        return InstituteUnit.objects.prefetch_related("contracts__partnership__company").all()


@admin.register(UniversityContactPerson)
class UniversityContactPersonAdmin(ReadOnlyModelAdmin, admin.ModelAdmin):
    list_display = ["first_name", "last_name", "phone", "get_email_url", "academic_title"]
    fields = ["first_name", "last_name", "phone", "email", "academic_title", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]
    search_fields = ["first_name", "last_name", "phone", "academic_title"]
    inlines = [UniversityContactPersonToInstituteUnitInlineAdmin]

    def autocomplete_view(self, request):
        return UniversityContactPersonAutocomplete.as_view(model_admin=self)(request)

    def get_email_url(self, obj: UniversityContactPerson):
        return format_html('<a href="%s">%s' % (obj.id, obj.email))

    get_email_url.allow_tags = True
    get_email_url.short_description = 'Email'
