from django.urls import path
from . import views

urlpatterns = [
    path('', views.separate_instruments, name='separate_instruments'),
]

