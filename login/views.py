from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm


class userFormView(View):
    form_class = UserForm
    template_name = 'login/registration_form.html'

    def get(self, reqest):
        form =self.form_class(None)
        return render(reqest, self.template_name, {'form': form})

    # prosses form data
    def post(self, reqest):
        form =self.form_class(reqest.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login (reqest, user)
                return redirect('/api')
                
        return render(reqest, self.template_name, {'form': form})


