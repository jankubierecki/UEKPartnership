from django.contrib import admin
from django.contrib.admin import DateFieldListFilter, AllValuesFieldListFilter, ChoicesFieldListFilter
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from common.admin import ReadOnlyModelAdmin
from company.models import CompanyContactPerson
from partnerships.models import Partnership, Contract
from university.models import UniversityContactPerson


class ContractInlineAdmin(ReadOnlyModelAdmin, admin.StackedInline):
    model = Contract
    extra = 1
    max_num = 1
    min_num = 1
    can_delete = True
    fields = ['partnership', 'company', 'institute_unit', 'contract_date', 'contract_number', 'amount',
              'additional_info']
    autocomplete_fields = ["institute_unit", "company"]


# todo add all links
@admin.register(Partnership)
class PartnershipAdmin(ReadOnlyModelAdmin, admin.ModelAdmin):
    inlines = [ContractInlineAdmin]
    search_fields = ['contract_date', 'last_contract_date', 'university_contact_person']
    list_display = ['name', 'get_company_name', 'get_institute_unit_name', 'contract_date', 'last_contact_date',
                    'kind_of_partnership', 'type_of_partnership']
    fields = ['name', 'contract_date', 'last_contact_date', 'university_contact_person', 'company_contact_person',
              'kind_of_partnership', 'type_of_partnership']
    create_fields = ['contract_date', 'last_contact_date', "name", "kind_of_partnership", "type_of_partnership"]
    list_filter = (
        ('contract_date', DateFieldListFilter),
        ('university_contact_person', RelatedDropdownFilter),
        ('type_of_partnership', ChoicesFieldListFilter),
        ('kind_of_partnership', ChoicesFieldListFilter),

    )

    # autocomplete_fields = ['university_contact_person', 'company_contact_person']

    def get_company_name(self, obj: Partnership):
        return obj.contract.company.name

    get_company_name.short_description = "Firma współpracująca"

    def get_institute_unit_name(self, obj: Partnership):
        return obj.contract.institute_unit.name

    get_institute_unit_name.short_description = "Nazwa jednostki UEK"

    def get_fields(self, request, obj=None):
        if obj is None:
            return self.create_fields
        return self.fields

    def get_form(self, request, obj=None, **kwargs):
        form = super(PartnershipAdmin, self).get_form(request, obj, **kwargs)
        if obj is not None and 'company_contact_person' in form.base_fields and 'university_contact_person' in form.base_fields:
            form.base_fields['company_contact_person'].queryset = CompanyContactPerson.objects.filter(
                companytocompanycontactperson__company=obj.contract.company)
            form.base_fields['university_contact_person'].queryset = UniversityContactPerson.objects.filter(
                instituteunit=obj.contract.institute_unit)
        return form
