from django.urls import path
from . import views

urlpatterns = [
    path('', views.calculate_deposit, name='calculate_deposit'),
    path('', views.index, name='calculate_deposit'),
]