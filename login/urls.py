from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.userFormView.as_view(), name="login"),
    path("/logout", views.logout_view, name="logout")
]