from django.http import HttpResponse
from django.views import View


class ErrorEmailTest(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=500, content="Testing 500")
