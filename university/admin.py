from django.contrib import admin
from django.utils.html import format_html

from university.models import UniversityFaculty, Institute, InstituteUnit, UniversityContactPerson, \
    InstituteUnitToUniversityContactPerson


# set Institute in TabularInline, aka Katedra, which will be pinned into UniversityFaculty, aka Wydział
class InstituteInlineAdmin(admin.TabularInline):
    model = Institute
    extra = 0
    can_delete = True


# register UniversityFaculty, aka Wydział with Institute
@admin.register(UniversityFaculty)
class UniversityFacultyAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [InstituteInlineAdmin]


# set TabularInline relation between Jednostka Współpracująca and Jednostka do kontaktu UEK
class InstituteUnitToUniversityContactPersonInlineAdmin(admin.TabularInline):
    model = InstituteUnitToUniversityContactPerson
    extra = 0
    verbose_name_plural = "Przypisane osoby"
    fields = ['university_contact_person', 'created_at']
    readonly_fields = ['created_at']


# set Osoba do kontaktu UEK panel in Jednostka Współpracująca admin view
class UniversityContactPersonToInstituteUnitInlineAdmin(InstituteUnitToUniversityContactPersonInlineAdmin):
    fields = ['institute_unit', 'created_at']
    can_delete = False
    readonly_fields = ['institute_unit', 'created_at']
    verbose_name_plural = "Przypisane jednostki współpracujące UEK"

    def has_add_permission(self, request):
        return False


# register InstituteUnit, aka Jednostka Współpracująca
@admin.register(InstituteUnit)
class InstituteUnitAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "updated_at", "get_institute_name"]
    search_fields = ["name", "institute__name"]
    list_filter = ["institute", "created_at", "updated_at"]
    fields = ["name", "institute", "created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]
    filter_horizontal = ['university_contact_persons']
    inlines = [InstituteUnitToUniversityContactPersonInlineAdmin]

    def get_institute_name(self, obj: InstituteUnit):
        if obj.institute is not None:
            return obj.institute.name
        else:
            return ""

    get_institute_name.short_description = "Katedra"


# register UniversityContactPerson, aka Osoby Do kontaktu UEK
@admin.register(UniversityContactPerson)
class UniversityContactAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "phone", "get_email_url", "academic_title"]
    fields = ["first_name", "last_name", "phone", "email", "academic_title", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]
    search_fields = list_display
    inlines = [UniversityContactPersonToInstituteUnitInlineAdmin]

    # change plain text email in Osoba do kontaktu UEK admin view, to link which points to specific Person
    def get_email_url(self, obj: UniversityContactPerson):
        return format_html('<a href="%s">%s' % (obj.id, obj.email))

    get_email_url.allow_tags = True
    get_email_url.short_description = 'Email'
