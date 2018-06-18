from django.contrib import admin
from django.contrib.admin import DateFieldListFilter, ChoicesFieldListFilter
from django.contrib.auth.models import User
from django.forms import Textarea
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from django.db import models

from common.admin import ReadOnlyModelAdmin
from company.models import CompanyContactPerson
from partnerships.models import Partnership, Contract, PartnershipLogEntry
from university.models import UniversityContactPerson


class PartnershipLogEntryInlineAdmin(ReadOnlyModelAdmin, admin.TabularInline):
    model = PartnershipLogEntry
    extra = 1
    can_delete = False
    fields = ['description', 'created_at', 'updated_at', 'created_by', 'updated_by']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': '3', 'cols': 60})},
    }


class ContractInlineAdmin(ReadOnlyModelAdmin, admin.StackedInline):
    model = Contract
    extra = 1
    max_num = 1
    min_num = 1
    can_delete = False
    fields = ['partnership', 'company', 'institute_unit', 'contract_date', 'contract_number', 'amount',
              'additional_info']
    autocomplete_fields = ["institute_unit", "company"]


@admin.register(Partnership)
class PartnershipAdmin(ReadOnlyModelAdmin, admin.ModelAdmin):
    inlines = [ContractInlineAdmin, PartnershipLogEntryInlineAdmin]
    change_form_template = "admin/partnership_change_form.html"
    change_list_template = "admin/partnership_change_list.html"
    search_fields = ['contract_date', 'last_contact_date', 'university_contact_person__first_name',
                     'university_contact_person__last_name', 'company_contact_person__first_name',
                     'company_contact_person__last_name', 'contract__company__name', ]
    list_display = ['name', 'get_company_name', 'get_company_contact_person_name_url', 'get_institute_unit_name',
                    'get_university_contact_person_name_url', 'contract_date', 'last_contact_date',
                    'get_status_with_color', 'get_author_name']
    fields = ['name', 'contract_date', 'last_contact_date', 'company_contact_person', 'university_contact_person',
              'kind_of_partnership', 'type_of_partnership', 'status']
    list_filter = (
        ('contract_date', DateFieldListFilter),
        ('university_contact_person', RelatedDropdownFilter),
        ('company_contact_person', RelatedDropdownFilter),
        ('type_of_partnership', ChoicesFieldListFilter),
        ('kind_of_partnership', ChoicesFieldListFilter),
        ('status', ChoicesFieldListFilter),
    )
    status_html = {
        'finished': '<div style="width:100%%; height:100%%; color:grey;">%s</div>',
        'paid_and_on': '<div style="width:100%%; height:100%%; color:green;">%s</div>',
        'started_not_paid': '<div style="width:100%%; height:100%%; color:red;">%s</div>',
        'other': '<div style="width:100%%; height:100%%; color:purple;">%s</div>',
    }

    autocomplete_fields = ['university_contact_person', 'company_contact_person']

    # todo validate if  is null
    # todo validae example@uek.krakow - placeholder and exclude this from possible email choices
    # todo display name and surname, not login

    def save_formset(self, request, form, formset, change):
        if formset.model == PartnershipLogEntry:
            entries = formset.save(commit=False)
            for log in entries:
                if log.id is None:
                    log.created_by = request.user
                    log.updated_by = request.user
                else:
                    log.updated_by = request.user
                log.save()
            formset.save_m2m()

        else:
            super(PartnershipAdmin, self).save_formset(request, form, formset, change)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

    def get_author_name(self, obj: Partnership):
        credentials = User.objects.distinct().filter(id=obj.author.id).values('first_name',
                                                                              'last_name').get()
        return ' '.join(credentials.values())

    get_author_name.short_description = "Autor"

    def get_company_name(self, obj: Partnership):
        return mark_safe(
            '<a href="{}">{}</a>'.format(reverse("admin:company_company_change", args=(obj.contract.company.pk,)),
                                         obj.contract.company.name))

    get_company_name.short_description = "Firma współpracująca"

    def get_institute_unit_name(self, obj: Partnership):
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse("admin:university_instituteunit_change", args=(obj.contract.institute_unit.pk,)),
                obj.contract.institute_unit.name))

    get_institute_unit_name.short_description = "Nazwa jednostki UEK"

    def get_university_contact_person_name_url(self, obj: Partnership):
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse("admin:university_universitycontactperson_change", args=(obj.university_contact_person.id,)),
                obj.university_contact_person.email))

    get_university_contact_person_name_url.short_description = "Osoba do kontaktu UEK"

    def get_company_contact_person_name_url(self, obj: Partnership):
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse("admin:company_companycontactperson_change", args=(obj.company_contact_person.id,)),
                obj.company_contact_person.email))

    get_company_contact_person_name_url.short_description = "Osoba do kontaktu Firmy"

    def get_status_with_color(self, obj: Partnership):
        return mark_safe(self.status_html.get(obj.status) % obj.get_status_display())

    get_status_with_color.short_description = "Status"

    def get_form(self, request, obj=None, **kwargs):
        form = super(PartnershipAdmin, self).get_form(request, obj, **kwargs)
        if obj is not None and 'company_contact_person' in form.base_fields and 'university_contact_person' in form.base_fields:
            if request.POST:
                company_id = int(request.POST['contract-0-company'])
                institute_unit_id = int(request.POST['contract-0-institute_unit'])
                form.base_fields['company_contact_person'].queryset = CompanyContactPerson.objects.filter(
                    companytocompanycontactperson__company_id=company_id)
                form.base_fields['university_contact_person'].queryset = UniversityContactPerson.objects.filter(
                    institute_units__institute_unit=institute_unit_id)
            else:
                form.base_fields['company_contact_person'].queryset = CompanyContactPerson.objects.filter(
                    companytocompanycontactperson__company=obj.contract.company)
                form.base_fields['university_contact_person'].queryset = UniversityContactPerson.objects.filter(
                    institute_units__institute_unit=obj.contract.institute_unit)
        return form
