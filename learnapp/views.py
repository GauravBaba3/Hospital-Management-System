from django.shortcuts import render, redirect,get_object_or_404
from learnapp.forms import UserForm, UserProfileForm
from learnapp.models import UserDetails
from learnapp.forms import UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from labreports.models import LabTechnician
from django.contrib import messages

# Create your views here.
def registration(request):
    registered = False
    if request.method == "POST":
        form1 = UserForm(request.POST)
        form2 = UserProfileForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()

            profile = form2.save(commit=False)
            profile.user = user # merging the form 1 and form 2 data
            profile.save()
            registered = True
    else:
        form1 = UserForm()
        form2 = UserProfileForm()

    context = {
        'form1':form1,
        'form2':form2,
        'registered': registered
    }
    return render(request, 'registration.html', context)







# user login view
def user_login(request):
    wrong_cred = False
    labtech1 = False
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password) # it will handle the password and user name, even the password is encrypted then also it will take care of it.
        if user:
            if user.is_active:
                login(request, user)
                return redirect('doctorshome')
            else:
                messages.error(request, "Oops! User is not active..!!")
        else:
            messages.error(request, "Oops! You have Entered Wrong credentials..!!")
            wrong_cred = True
    return render(request, 'login.html', {'labtech1':labtech1, 'wrong_cred':wrong_cred})




# this is home view
@login_required(login_url='login')
def home(request):
    return render(request, 'doctors/home.html', {})




# this is profile
@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html', {})




@login_required(login_url="login")
def update_user_details(request):
    user_details = get_object_or_404(UserDetails, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(
            request.POST,
            request.FILES,   # ⚠️ image ke liye important
            instance=user_details
        )
        print("1")
        if form.is_valid():
            form.save()
            return redirect('profile')  # apna page
    else:
        print("2")
        form = UserProfileForm(instance=user_details)

    return render(request, 'update_user_details.html', {'form': form})



# this is logout
@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')