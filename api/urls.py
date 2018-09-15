from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("history", views.HistoryView.as_view(), name='history')
]