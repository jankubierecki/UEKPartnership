from django.contrib.admin.views.autocomplete import AutocompleteJsonView


class BaseAutocomplete(AutocompleteJsonView):
    parent_id = None

    def get(self, request, *args, **kwargs):
        self.parent_id = request.GET.get("parent_id")

        return super(BaseAutocomplete, self).get(request, *args, **kwargs)


class UniversityContactPersonAutocomplete(BaseAutocomplete):

    def get_queryset(self):
        queryset = super(UniversityContactPersonAutocomplete, self).get_queryset()
        if self.parent_id is not None:
            return queryset.filter(
                institute_units__institute_unit_id=self.parent_id
            )
        return queryset


class CompanyContactPersonAutocomplete(BaseAutocomplete):

    def get_queryset(self):
        queryset = super(CompanyContactPersonAutocomplete, self).get_queryset()
        if self.parent_id is not None:
            return queryset.filter(
                companytocompanycontactperson=self.parent_id
            )
        return queryset
