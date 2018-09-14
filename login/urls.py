from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.userFormView.as_view(), name="login"),
]