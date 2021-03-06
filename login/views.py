from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm, ProfileForm, LoginnForm
from django.core.mail import send_mail
from django.conf import settings


class UserFormView(View):
    user_form = UserForm
    profile_form = ProfileForm

    template_name = 'login/registration_form.html'

    def get(self, request):
        userForm =self.user_form(None)
        profileForm = self.profile_form(None)
        return render(request, self.template_name, {'user_form': userForm, 'profile_form': profileForm})

    # prosses form data
    def post(self, request):
        userForm =self.user_form(request.POST)
        if userForm.is_valid():
            user = userForm.save()
            user.set_password(userForm.cleaned_data['password'])
            user.save()
            profileForm = ProfileForm(request.POST, instance=user.profile)
            profileForm.save()

            if user is not None and user.is_active:
                login (request, user)
                email(userForm.cleaned_data['email'])
                return redirect('/')
                
        return render(request, self.template_name, {'user_form': userForm, 'profile_form': profileForm})

class LoginView(View):
    form = LoginnForm
    template_name = 'login/login_form.html'
    def get(self, request):
        form =self.form(None)
        return render(request, self.template_name, { 'form': form })

    def post(self, request):
        form = self.form(request.POST)

        if form.is_valid():


            #cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # user.set_password(password) #this is the only way to change a password because of hashing

            #returns the User obejects if credintials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')


        return render(request, self.template_name,{'form': form})

    
def logoutView(request):
    logout(request)
    return redirect('/')

def email(userEmail):

    subject = 'Thank you for registering to weather app'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [userEmail,]

    send_mail( subject, message, email_from, recipient_list )
    return

