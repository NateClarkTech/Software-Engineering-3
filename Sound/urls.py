from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.sound, name='sound'),
    path('<str:label_name>/', views.label_sort, name='sound_label_sort'),
    ]
