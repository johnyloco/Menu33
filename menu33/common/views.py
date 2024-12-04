from django.shortcuts import render


def home_page(request):
    return render(request, 'common/home-page.html')


def home(request):
    return render(request, 'common/home.html')


