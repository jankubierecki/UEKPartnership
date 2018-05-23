from django.contrib import admin

from university.models import UniversityFaculty, Institute, InstituteUnit


class InstituteInlineAdmin(admin.TabularInline):
    model = Institute
    extra = 0


@admin.register(UniversityFaculty)
class UniversityFacultyAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [InstituteInlineAdmin]


@admin.register(InstituteUnit)
class InstituteUnitAdmin(admin.ModelAdmin):
    list_display = ["get_institute_name", "name", "created_at", "updated_at"]
    list_filter = ["institute", "created_at", "updated_at"]
    fields = ["name", "institute", "created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]

    def get_institute_name(self, obj:InstituteUnit):
        if obj.institute is not None:
            return obj.institute.name
        else:
            return ""

    get_institute_name.short_description = "Katedra"
