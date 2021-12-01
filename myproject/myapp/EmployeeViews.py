from django.shortcuts import render


def employee_home(request):
    return render(request,"employee_template/employee_home_template.html")