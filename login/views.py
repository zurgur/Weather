from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm, ProfileForm


class userFormView(View):
    user_form = UserForm
    profile_form = ProfileForm

    template_name = 'login/registration_form.html'

    def get(self, request):
        userForm =self.user_form(None)
        profileForm = self.profile_form(None)
        return render(request, self.template_name, {'user_form': userForm, 'profile_form': profileForm})

    # prosses form data
    def post(self, request):
        userForm =self.user_form(request.POST, instance=request.user)
        profileForm = self.profile_form(request.POST, instance=request.user.profile)
        if userForm.is_valid() and profileForm.is_valid():
            user = userForm.save(commit=False)

            username = userForm.cleaned_data['username']
            password = userForm.cleaned_data['password']
            user.set_password(password)
            user.save()
            profileForm.save()

            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login (request, user)
                return redirect('/')
                
        return render(request, self.template_name, {'user_form': userForm, 'profile_form': profileForm})

    
def logout_view(request):
    logout(request)
    return redirect('/')


