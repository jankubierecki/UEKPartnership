import datetime

from django.contrib import admin
from django.contrib.admin import DateFieldListFilter, ChoicesFieldListFilter
from django.core.exceptions import ValidationError
import django.forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from django.db import models

from common.admin import ReadOnlyModelAdmin

from partnerships.models import Partnership, Contract, PartnershipLogEntry


class ContractInlineForm(django.forms.ModelForm):
    """ validates contract date form also in the terms of partnership dates forms validation """

    class Meta:
        model = Contract
        fields = ['contract_date']

    def clean(self):
        contract_date = self.cleaned_data.get('contract_date')
        partnership_start_date = self.cleaned_data['partnership'].start_date
        partnership_last_contact_date = self.cleaned_data['partnership'].last_contact_date

        if partnership_last_contact_date is not None and partnership_start_date is not None:

            if contract_date is not None:
                if partnership_start_date > contract_date:
                    raise ValidationError('Data zawiązania umowy nie może być starsza od daty rozpoczęcia współpracy.')

                if partnership_last_contact_date < contract_date:
                    raise ValidationError(
                        'Zaktualizuj także datę ostatniego kontaktu współpracy - data zawiązania umowy może być mniejsza lub równa tej dacie.')

        else:
            return

        return self.cleaned_data


class ContractInlineAdmin(ReadOnlyModelAdmin, admin.StackedInline):
    model = Contract
    extra = 0
    min_num = 0
    can_delete = False
    fields = ['partnership', 'institute_unit',
              'contract_date', 'contract_number', 'amount_pay',
              'additional_info', 'company_contact_persons', 'university_contact_persons']
    autocomplete_fields = ["institute_unit", 'company_contact_persons', 'university_contact_persons']
    form = ContractInlineForm


class PartnershipLogEntryInlineAdmin(ReadOnlyModelAdmin, admin.TabularInline):
    model = PartnershipLogEntry
    extra = 1
    can_delete = False
    fields = ['description', 'created_at', 'updated_at', 'created_by', 'updated_by']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    formfield_overrides = {
        models.TextField: {'widget': django.forms.Textarea(attrs={'rows': '3', 'cols': 60})},
    }


class PartnershipModelForm(django.forms.ModelForm):
    """ validates partnership dates forms without contract """

    class Meta:
        model = Partnership
        fields = ['start_date', 'last_contact_date', 'status']

    def clean(self):

        try:

            start_date = self.cleaned_data['start_date']
            last_contact_date = self.cleaned_data['last_contact_date']
            status = self.cleaned_data['status']

        except KeyError:
            return

        current_date = datetime.date.today()

        if start_date > last_contact_date:
            raise ValidationError('Data ostatniego kontaktu nie może być starsza od daty rozpoczęcia współpracy.')

        if start_date <= current_date < last_contact_date:
            raise ValidationError(
                'Data ostaniego kontaktu nie może wybiegać w przyszłość jeśli data rozpoczęcia jest starsza lub równa dzisiejszej dacie.')

        if current_date < start_date != last_contact_date:
            raise ValidationError(
                'Data ostatniego kontaktu musi być równa dacie rozpoczęcia współpracy jeśli obie są z przyszłości. Ustaw obie daty na ten sam dzień, lub z rezygnuj z przyszłościowych dat.')

        if last_contact_date > current_date and status == 'finished':
            raise ValidationError(
                "Status współpracy 'zakończona' jest dopuszczalny tylko wtedy, gdy data rozpoczęcia i data ostatniego kontaktu są z przeszłości.")

        return self.cleaned_data


@admin.register(Partnership)
class PartnershipAdmin(ReadOnlyModelAdmin, admin.ModelAdmin):
    inlines = [ContractInlineAdmin, PartnershipLogEntryInlineAdmin]
    form = PartnershipModelForm
    change_form_template = "admin/partnership_change_form.html"
    search_fields = ['start_date', 'last_contact_date', 'contracts__university_contact_persons__first_name',
                     'contracts__institute_unit__name',
                     'contracts__university_contact_persons__last_name',
                     'contracts__company_contact_persons__first_name',
                     'contracts__company_contact_persons__last_name', 'company', 'name']
    list_display = ['name', 'get_company_name',
                    'get_institute_unit_name', 'get_company_contact_persons', 'get_university_contact_persons',
                    'start_date', 'last_contact_date',
                    'get_status_with_color']
    fields = ['name', 'company', 'start_date', 'last_contact_date',
              'kind_of_partnership', 'type_of_partnership', 'status', 'author']

    readonly_fields = ['author']

    status_html = {
        'finished': '<div style="width:100%%; height:100%%; color:grey;">%s</div>',
        'unfinished': '<div style="width:100%%; height:100%%; color:green;">%s</div>',
    }

    autocomplete_fields = ['company']

    list_filter = (
        ('start_date', DateFieldListFilter),
        ('company', RelatedDropdownFilter),
        ('type_of_partnership', ChoicesFieldListFilter),
        ('kind_of_partnership', ChoicesFieldListFilter),
        ('status', ChoicesFieldListFilter),
    )

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
        if obj.id is None:
            obj.author = request.user

        obj.save()

    def get_author_name(self, obj: Partnership):
        if obj.author is None:
            return " "
        return "%s %s" % (obj.author.first_name, obj.author.last_name)

    get_author_name.short_description = "Autor"

    def get_company_name(self, obj: Partnership):
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse("admin:company_company_change", args=(obj.company.pk,)),
                obj.company.name))

    get_company_name.short_description = "Firma współpracująca"

    def get_institute_unit_name(self, obj: Partnership):
        if obj.contracts.filter(partnership=obj.pk).count() == 0:
            return "brak"
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse("admin:university_instituteunit_change",
                        args=(obj.contracts.all().last().institute_unit.pk,)),
                obj.contracts.all().last().institute_unit.name, ))

    get_institute_unit_name.short_description = "Jednostka UEK"

    def get_university_contact_persons(self, obj: Partnership):

        if obj.contracts.filter(partnership=obj.pk).count() == 0:
            return "brak"

        full_names = zip(obj.contracts.latest().university_contact_persons.all().values('first_name'),
                         obj.contracts.latest().university_contact_persons.all().values('last_name'),
                         obj.contracts.latest().university_contact_persons.all().values('id')
                         )
        html = ""
        index = 1

        for first_name, last_name, ids in full_names:
            html += " " + str(index) + ". " + mark_safe(
                '<a href="{}">{}{}{}</a>'.format(
                    reverse("admin:university_universitycontactperson_change",
                            args=(obj.contracts.latest().university_contact_persons.get(
                                id=ids.get('id')).id,)),
                    first_name.get('first_name'), " ",
                    last_name.get('last_name'), ))
            index += 1
        return mark_safe(html)

    get_university_contact_persons.short_description = "Osoby do kontaktu UEK"

    def get_company_contact_persons(self, obj: Partnership):

        if obj.contracts.filter(partnership=obj.pk).count() == 0:
            return "brak"

        full_names = zip(obj.contracts.latest().company_contact_persons.all().values('first_name'),
                         obj.contracts.latest().company_contact_persons.all().values('last_name'),
                         obj.contracts.latest().company_contact_persons.all().values('id'))

        html = ""
        index = 1

        for first_name, last_name, ids in full_names:
            html += " " + str(index) + ". " + mark_safe(
                '<a href="{}">{}{}{}</a>'.format(
                    reverse("admin:company_companycontactperson_change",
                            args=(obj.contracts.latest().company_contact_persons.get(
                                id=ids.get('id')).id,)),
                    first_name.get('first_name'), " ",
                    last_name.get('last_name'), ))
            index += 1
        return mark_safe(html)

    get_company_contact_persons.short_description = "Osoby do kontaktu Firmy"

    def get_status_with_color(self, obj: Partnership):
        if obj.status is None:
            return "Nieznana"
        return mark_safe(self.status_html.get(obj.status) % obj.get_status_display())

    get_status_with_color.short_description = "Status"
