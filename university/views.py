from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from django.views import View

from partnerships.models import Partnership


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
                instituteunit=self.parent_id
            )
        return queryset


class CompanyContactPersonAutocomplete(BaseAutocomplete):

    def get_queryset(self):
        queryset = super(CompanyContactPersonAutocomplete, self).get_queryset()
        if self.parent_id is not None:
            return queryset.filter(
                companies=self.parent_id
            )
        return queryset


class PartnershipAutocomplete(View):
    def get_queryset(self, request, q):
        partnership_id = request.GET.get("id")
        if partnership_id is not None:
            return Partnership.objects.filter(q).exclude(id=partnership_id).distinct().values("name", "id")[:5]
        else:
            return Partnership.objects.filter(q).distinct().values("name", "id")[:5]

    def get(self, request, *args, **kwargs):
        query = request.GET.get("term")
        if query is None or len(query) < 3:
            return JsonResponse([], safe=False)
        split_query = query.split(" ")
        q = Q()
        for term in split_query:
            q |= Q(name__icontains=term)
        partnerships = list(self.get_queryset(request, q))
        for partnership in partnerships:
            partnership["url"] = reverse("admin:partnerships_partnership_change", args=[partnership.get("id")])

        return JsonResponse(partnerships, safe=False,)
