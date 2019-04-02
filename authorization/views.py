from django.shortcuts import render, redirect


def next_page(request):
    if request.user.is_staff:
        return render(request, '')

    return render(request, 'authorization/next_page.html')
