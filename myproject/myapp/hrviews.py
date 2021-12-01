from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from myapp.forms import AddEmployersForm, EditEmployersForm
from myapp.models import CustomUser, Employee, Destination, Subjects, Employers


def admin_home(request):
    return render(request,"hod_template/home_content.html")

def add_employee(request):
    return render(request,"hod_template/add_staff_template.html")

def add_employer_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))

def add_destination(request):
    return render(request,"hod_template/add_destination_template.html")

def add_destination_save(request, destination=None):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course=request.POST.get("destination")
        try:
            course_model=Destination(destination_name=destination)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect(reverse("add_course"))

def add_employers(request):
    form=AddEmployersForm()
    return render(request,"hod_template/add_student_template.html",{"form":form})

def add_employers_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddEmployersForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            address=form.cleaned_data["address"]
            session_start=form.cleaned_data["session_start"]
            session_end=form.cleaned_data["session_end"]
            destination_id=form.cleaned_data["destination"]
            sex=form.cleaned_data["sex"]

            profile_pic=request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)

            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                user.employers.address=address
                employers_obj=Destination.objects.get(id=destination_id)
                user.employers.employers_id=employers_obj
                user.employers.session_start_year=session_start
                user.employers.session_end_year=session_end
                user.employers.gender=sex
                user.employers.profile_pic=profile_pic_url
                user.save()
                messages.success(request,"Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request,"Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form=AddEmployersForm(request.POST)
            return render(request, "hod_template/add_student_template.html", {"form": form})


def add_subject(request):
    destination=Destination.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/add_subject_template.html",{"staffs":staffs,"courses":destination})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name=request.POST.get("subject_name")
        destination_id=request.POST.get("course")
        destination=Destination.objects.get(id=destination_id)
        employee_id=request.POST.get("staff")
        staff=CustomUser.objects.get(id=employee_id)

        try:
            subject=Subjects(subject_name=subject_name,destination_id=destination,employee_id=employee)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))


def manage_employee(request):
    employee=Employee.objects.all()
    return render(request,"hr_template/manage_employee_template.html",{"employee":employee})

def manage_employers(request):
    employers=Employers.objects.all()
    return render(request,"hr_template/manage_employer_template.html",{"employers":employers})

def manage_destination(request):
    destination=Destination.objects.all()
    return render(request,"hr_template/manage_destination_template.html",{"destination":destination})

def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request,"hod_template/manage_subject_template.html",{"subjects":subjects})

def edit_employee(request,employee_id):
    staff=Employee.objects.get(admin=employee_id)
    return render(request,"hod_template/edit_staff_template.html",{"staff":staff,"id":employee_id})

def edit_employee_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        employee_id=request.POST.get("employee_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=employee_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            employee_model=Employee.objects.get(admin=employee_id)
            employee_model.address=address
            employee_model.save()
            messages.success(request,"Successfully Edited Employee")
            return HttpResponseRedirect(reverse("edit_employee",kwargs={"employee_id":employee_id}))
        except:
            messages.error(request,"Failed to Edit Employee")
            return HttpResponseRedirect(reverse("edit_employee",kwargs={"staff_id":employee_id}))

def edit_employers(request,employers_id):
    request.session['employers_id']=employers_id
    employers=Employers.objects.get(admin=employers_id)
    form=EditEmployersForm()
    form.fields['email'].initial=employers.admin.email
    form.fields['first_name'].initial=employers.admin.first_name
    form.fields['last_name'].initial=employers.admin.last_name
    form.fields['username'].initial=employers.admin.username
    form.fields['address'].initial=employers.address
    form.fields['destination'].initial=employers.destination_id.id
    form.fields['sex'].initial=employers.gender
    form.fields['session_start'].initial=employers.session_start_year
    form.fields['session_end'].initial=employers.session_end_year
    return render(request,"hod_template/edit_employers_template.html",{"form":form,"id":employers_id,"username":employers.admin.username})

def edit_employers_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        employers_id=request.session.get("employers_id")
        if employers_id==None:
            return HttpResponseRedirect(reverse("manage_student"))

        form=EditEmployersForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_start = form.cleaned_data["session_start"]
            session_end = form.cleaned_data["session_end"]
            destination_id = form.cleaned_data["destination"]
            sex = form.cleaned_data["sex"]

            if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None


            try:
                user=CustomUser.objects.get(id=employers_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                employers=Employers.objects.get(admin=employers_id)
                employers.address=address
                employers.session_start_year=session_start
                employers.session_end_year=session_end
                employers.gender=sex
                destination=Employers.objects.get(id=employers_id)
                employers.destination_id=destination
                if profile_pic_url!=None:
                    employers.profile_pic=profile_pic_url
                employers.save()
                del request.session['employers_id']
                messages.success(request,"Successfully Edited Employer")
                return HttpResponseRedirect(reverse("edit_employers",kwargs={"employer_id":employers_id}))
            except:
                messages.error(request,"Failed to Edit Employer")
                return HttpResponseRedirect(reverse("edit_employer",kwargs={"employer_id":employers_id}))
        else:
            form=EditEmployersForm(request.POST)
            employers=Employers.objects.get(admin=employers_id)
            return render(request,"hod_template/edit_employers_template.html",{"form":form,"id":employers_id,"username":employers.admin.username})

def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    destination=Destination.objects.all()
    employee=CustomUser.objects.filter(user_type=2)
    return render(request,"hr_template/edit_subject_template.html",{"subject":subject,"employee":employee,"destination":destination,"id":subject_id})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        employee_id=request.POST.get("employee")
        destination_id=request.POST.get("destination")

        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            employee=CustomUser.objects.get(id=employee_id)
            subject.employee_id=employee
            destination=Destination.objects.get(id=destination_id)
            subject.destination_id=destination
            subject.save()

            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))


def edit_destination(request,destination_id):
    destination=Destination.objects.get(id=destination_id)
    return render(request,"hr_template/edit_course_template.html",{"destination":destination,"id":destination_id})

def edit_destination_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        destination_id=request.POST.get("destination_id")
        destination_name=request.POST.get("destination")

        try:
            destination=Destination.objects.get(id=destination_id)
            destination.destination_name=destination_name
            destination.save()
            messages.success(request,"Successfully Edited Destination")
            return HttpResponseRedirect(reverse("edit_destination",kwargs={"destination_id":destination_id}))
        except:
            messages.error(request,"Failed to Edit Destination")
            return HttpResponseRedirect(reverse("edit_destination",kwargs={"destination_id":destination_id}))

