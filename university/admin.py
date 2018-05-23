from django.contrib import admin

from university.models import UniversityFaculty, Institute, InstituteUnit, UniversityContactPerson, \
    InstituteUnitToUniversityContactPerson


class InstituteInlineAdmin(admin.TabularInline):
    model = Institute
    extra = 0


@admin.register(UniversityFaculty)
class UniversityFacultyAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [InstituteInlineAdmin]


class InstituteUnitToUniversityContactPersonInlineAdmin(admin.TabularInline):
    model = InstituteUnitToUniversityContactPerson
    extra = 0
    verbose_name_plural = "Przypisane osoby"
    fields = ['university_contact_person', 'created_at']
    readonly_fields = ['created_at']


class UniversityContactPersonToInstituteUnitInlineAdmin(InstituteUnitToUniversityContactPersonInlineAdmin):
    fields = ['institute_unit', 'created_at']
    can_delete = False
    readonly_fields = ['institute_unit', 'created_at']
    verbose_name_plural = "Przypisane jednostki współpracujące UEK"

    def has_add_permission(self, request):
        return False


@admin.register(InstituteUnit)
class InstituteUnitAdmin(admin.ModelAdmin):
    list_display = ["get_institute_name", "name", "created_at", "updated_at"]
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

# todo add email_href search: link list view django admin
@admin.register(UniversityContactPerson)
class UniversityContactAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "phone", "email", "academic_title"]
    fields = ["first_name", "last_name", "phone", "email", "academic_title", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]
    search_fields = list_display
    inlines = [UniversityContactPersonToInstituteUnitInlineAdmin]

