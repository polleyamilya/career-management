from django.shortcuts import render


def employers_home(request):
    return render(request,"employers_template/employers_home_template.html")