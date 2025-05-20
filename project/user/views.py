from django.shortcuts import render, redirect
from .forms import customUserCreationForm,peopleForm,complaintForm,ProfileUpdateForm,userprofileupdate
from .forms import statusupdate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout ,update_session_auth_hash
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from .models import people,complaints
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404 
# Create your views here.


def hello(request):
    #return HttpResponse("hello everyone")
    return render(request,'index.html')

from django.shortcuts import render
from django.http import HttpResponse
from .forms import customUserCreationForm, peopleForm

#registration view
def register1(request):
    if request.method == 'POST':
        form = customUserCreationForm(request.POST)
        form2 = peopleForm(request.POST)
        if form.is_valid() and form2.is_valid():
            user = form.save()
            people = form2.save(commit=False)
            people.user = user
            people.save()
            messages.success(request, "Registration successful!")
            return redirect('login')
        else:
            print("Form errors:", form.errors, form2.errors)  # For debugging

    else:
        form = customUserCreationForm()
        form2 = peopleForm()
    
    context = {'form': form, 'form2': form2}
    return render(request, 'register.html', context)

#login view

def logi(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)  # Redirect to login_redirect view
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, 'login.html')

@login_required
def login_redirect(request):
    if request.user.is_authenticated:
        if request.user.people.type_user == 'student':
            return redirect('user')
        elif request.user.people.type_user == 'grievance':
            return redirect('counter')
    else:
        return redirect('login')
    
#logout view
def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)

@login_required(login_url='login')
#user view
def complaintsub(request):
    if request.method=='POST':
        form=complaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)  # Don't save to DB yet
            complaint.user = request.user        # Assign the logged-in user
            complaint.save()                     # Now save to DB
            messages.success(request, "Complaint submitted successfully!")
            return redirect('user')  # Redirect to the same page or another page
        else:
            print("Form errors:", form.errors)
    else:
        form=complaintForm()
    context={'form':form}
    return render(request,'user.html',context)

@login_required(login_url='login')
def updateprofile(request):
    if request.method=='POST':
        form=userprofileupdate(request.POST,instance=request.user)
        form2=ProfileUpdateForm(request.POST,instance=request.user.people)
        if form.is_valid() and form2.is_valid():
            user = form2.save()
            people = form.save(commit=False)
            people.user = user
            people.save()
            messages.add_message(request,messages.SUCCESS, f'Updated Successfully')
            return redirect('profile')
        else:
            print("Form errors:", form.errors, form2.errors) 
    else:
        form2=ProfileUpdateForm(instance=request.user.people)
        form=userprofileupdate(instance=request.user)
    context={'form':form,'form2':form2}
    return render(request,'profile.html',context)

#for grievance user
@login_required(login_url='login')
def updateprofileg(request):
    if request.method=='POST':
        form=userprofileupdate(request.POST,instance=request.user)
        form2=ProfileUpdateForm(request.POST,instance=request.user.people)
        if form.is_valid() and form2.is_valid():
            user = form2.save()
            people = form.save(commit=False)
            people.user = user
            people.save()
            messages.add_message(request,messages.SUCCESS, f'Updated Successfully')
            return redirect('profileg')
        else:
            print("Form errors:", form.errors, form2.errors) 
    else:
        form2=ProfileUpdateForm(instance=request.user.people)
        form=userprofileupdate(instance=request.user)
    context={'form':form,'form2':form2}
    return render(request,'profileg.html',context)

@login_required(login_url='login')
def solvedlist(request):
    complaints_list = complaints.objects.filter(user=request.user, status='Resolved')
    context = {'complaints_list': complaints_list}
    return render(request, 'solvedlistuser.html', context)

@login_required(login_url='login')
def alllist(request):
    complaints_list = complaints.objects.filter(user=request.user).exclude(status='Resolved')
    context = {'complaints_list': complaints_list}
    return render(request, 'alllistuser.html', context)

@login_required(login_url='login')
def passwordchange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)  
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.add_message(request,messages.SUCCESS, f'Updated Successfully')
        else:
            print("Form errors:", form.errors)
    else:
        form = PasswordChangeForm(user=request.user)  
    context = {'form': form}
    return render(request, 'passwordchange.html', context)

#for grievance user
@login_required(login_url='login')
def passwordchangeg(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)  
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.add_message(request,messages.SUCCESS, f'Updated Successfully')
        else:
            print("Form errors:", form.errors)
    else:
        form = PasswordChangeForm(user=request.user)  
    context = {'form': form}
    return render(request, 'passwordchangeg.html', context)


#@login_required
@login_required(login_url='login')
def counter(request):
    total=complaints.objects.all().count()
    pending=complaints.objects.filter(status='Pending').count()
    resolved=complaints.objects.filter(status='Resolved').count()
    inprogress=complaints.objects.filter(status='In Progress').count()
    graphset=complaints.objects.values('type').annotate(
    total=Count('status'),
    solved=Count('status',filter=Q(status='Resolved')),
    pending=Count('status',filter=Q(status='Pending')),
    inprogress=Count('status',filter=Q(status='In Progress'))).order_by('type')
    args={
        'total':total,
        'pending':pending,
        'resolved':resolved,
        'inprogress':inprogress,
        'graphset':graphset
    }
    return render(request,'counter.html',args)

@login_required(login_url='login')
def allcomplaints(request):
    # Get all complaints except those already Resolved
    complaint_list = complaints.objects.exclude(status='Resolved')

    # Search and filter logic
    search_term = request.GET.get("search")
    type_filter = request.GET.get("drop")

    if type_filter:
        complaint_list = complaint_list.filter(type__icontains=type_filter)
    if search_term:
        complaint_list = complaint_list.filter(
            Q(type__icontains=search_term) |
            Q(subject__icontains=search_term) |
            Q(description__icontains=search_term)
        )

    # Status update logic via POST
    if request.method == 'POST':
        cid = request.POST.get('cid2')
        complaint_obj = get_object_or_404(complaints, id=cid)
        form = statusupdate(request.POST, instance=complaint_obj)

        if form.is_valid():
            form.save()
            messages.success(request, "Complaint status updated successfully.")
            return redirect('allcomplaints')  # URL name must match your urls.py
        else:
            messages.error(request, "Error updating the complaint.")

    else:
        form = statusupdate()

    context = {
        'complaint_list': complaint_list,
        'form': form,
        'search_term': search_term
    }

    return render(request, 'allcomplaints.html', context)

@login_required(login_url='login')
def solvedcomplaints(request):
    # Get all complaints except those already Resolved
    complaint_list = complaints.objects.filter(status='Resolved')

    # Search and filter logic
    search_term = request.GET.get("search")
    type_filter = request.GET.get("drop")

    if type_filter:
        complaint_list = complaint_list.filter(type__icontains=type_filter)
    if search_term:
        complaint_list = complaint_list.filter(
            Q(type__icontains=search_term) |
            Q(subject__icontains=search_term) |
            Q(description__icontains=search_term)
        )

    # Status update logic via POST
    if request.method == 'POST':
        cid = request.POST.get('cid2')
        complaint_obj = get_object_or_404(complaints, id=cid)
        form = statusupdate(request.POST, instance=complaint_obj)

        if form.is_valid():
            form.save()
            messages.success(request, "Complaint status updated successfully.")
            return redirect('solvedcomplaints')  # URL name must match your urls.py
        else:
            messages.error(request, "Error updating the complaint.")

    else:
        form = statusupdate()

    context = {
        'complaint_list': complaint_list,
        'form': form,
        'search_term': search_term
    }

    return render(request, 'solvedcomplaints.html', context)

# views.py
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas  # adjust this import based on your app structure

@login_required(login_url='login')
def generate_complaint_pdf(request, complaint_id):
    complaint = complaints.objects.get(id=complaint_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="complaint_{complaint.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4


    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2.0, height - 50, "Complaint Report")

    p.setFont("Helvetica", 12)
    y = height - 100
    line_spacing = 20

    p.drawString(100, y, f"Complaint ID: {complaint.id}")
    y -= line_spacing
    p.drawString(100, y, f"Type: {complaint.type} ")
    y -= line_spacing
    p.drawString(100, y, f"Subject: {complaint.subject}")
    y -= line_spacing
    p.drawString(100, y, f"Status: {complaint.status}")
    y -= line_spacing
    p.drawString(100, y, f"Date Submitted: {complaint.date.strftime('%Y-%m-%d %H:%M')}")
    y -= line_spacing
    p.drawString(100, y, f"Description: {complaint.description}")

    # Finish up
    p.showPage()
    p.save()

    return response


    





