from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.IdeaBoards_Home, name='IdeaBoards_Home'),
    path('<int:id>/', views.IdeaBoard_Detail, name='IdeaBoard_Detail'),
    path('<int:id>/<str:label>', views.IdeaBoard_Detail, name='IdeaBoard_Detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

