from django.contrib import admin

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


@admin.register(Partnership)
class PartnershipAdmin(ReadOnlyModelAdmin, admin.ModelAdmin):
    inlines = [ContractInlineAdmin]
    search_fields = ['contract_date', 'last_contract_date', 'university_contact_person', 'company_contact_person']
    list_display = ['contract_date', 'last_contact_date', 'university_contact_person', 'company_contact_person']
    fields = ['contract_date', 'last_contact_date', 'university_contact_person', 'company_contact_person']
    create_fields = ['contract_date', 'last_contact_date']
    list_filter = list_display

    def get_fields(self, request, obj=None):
        if obj is None:
            return self.create_fields
        return self.fields

    def get_form(self, request, obj=None, **kwargs):
        form = super(PartnershipAdmin, self).get_form(request, obj, **kwargs)
        if obj is not None:
            form.base_fields['company_contact_person'].queryset = CompanyContactPerson.objects.filter(
                companytocompanycontactperson__company=obj.contract.company)
            form.base_fields['university_contact_person'].queryset = UniversityContactPerson.objects.filter(
                instituteunit=obj.contract.institute_unit)
        return form
