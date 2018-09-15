from django.urls import path, include

from . import views

urlpatterns = [
    path("register", views.UserFormView.as_view(), name="register"),
    path("logout", views.logoutView, name="logout"),
    path("login", views.LoginView.as_view(), name="login"),

]