from django import template
from django.contrib.admin.templatetags.admin_list import result_list, result_headers, result_hidden_fields, ResultList, \
    items_for_result

register = template.Library()


def results(cl):
    if cl.formset:
        for res, form in zip(cl.result_list, cl.formset.forms):
            yield ResultList(form, items_for_result(cl, res, form))
    else:
        for res in cl.result_list:
            yield (ResultList(None, items_for_result(cl, res, None)), res)


@register.inclusion_tag("admin/institute_unit_change_list_results.html")
def result_list(cl):
    headers = list(result_headers(cl))
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1
    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': headers,
            'num_sorted_fields': num_sorted_fields,
            'results': list(results(cl))}
