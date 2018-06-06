from django.contrib import admin
from django.utils.html import format_html

from common.admin import ReadOnlyModelAdmin
from university.models import UniversityFaculty, Institute, InstituteUnit, UniversityContactPerson, \
    InstituteUnitToUniversityContactPerson
from university.views import UniversityContactPersonAutocomplete


@admin.register(Institute)
class InstituteAdmin(ReadOnlyModelAdmin, admin.ModelAdmin):
    fields = ["name", 'university_faculty']
    search_fields = ["name", "university_faculty__name"]


class InstituteInlineAdmin(ReadOnlyModelAdmin, admin.TabularInline):
    model = Institute
    fields = ['name']
    extra = 0
    can_delete = True


@admin.register(UniversityFaculty)
class UniversityFacultyAdmin(ReadOnlyModelAdmin, admin.ModelAdmin):
    list_display = ["name"]
    fields = ['name']
    inlines = [InstituteInlineAdmin]


class InstituteUnitToUniversityContactPersonInlineAdmin(ReadOnlyModelAdmin, admin.TabularInline):
    model = InstituteUnitToUniversityContactPerson
    extra = 0
    verbose_name_plural = "Przypisane osoby"
    fields = ['university_contact_person', 'created_at']
    readonly_fields = ['created_at']
    autocomplete_fields = ["university_contact_person"]


class UniversityContactPersonToInstituteUnitInlineAdmin(InstituteUnitToUniversityContactPersonInlineAdmin):
    fields = ['institute_unit', 'created_at']
    verbose_name_plural = "Przypisane jednostki współpracujące UEK"


@admin.register(InstituteUnit)
class InstituteUnitAdmin(ReadOnlyModelAdmin, admin.ModelAdmin):
    list_display = ["name", "get_institute_name", "created_at", "updated_at"]
    search_fields = ["name", "institute__name"]
    list_filter = ["institute", "created_at", "updated_at"]
    fields = ["name", "institute", "created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]
    filter_horizontal = ['university_contact_persons']
    inlines = [InstituteUnitToUniversityContactPersonInlineAdmin]
    autocomplete_fields = ["institute"]

    def get_queryset(self, request):
        return InstituteUnit.objects.select_related("institute").select_related("institute__university_faculty").all()

    def get_institute_name(self, obj: InstituteUnit):
        if obj.institute is not None:
            return obj.institute.name
        else:
            return ""

    get_institute_name.short_description = "Katedra"


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
