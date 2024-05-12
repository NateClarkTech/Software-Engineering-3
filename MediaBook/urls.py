"""
URL configuration for MediaBook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.conf import settings
from django.conf.urls.static import static
from Forum import views as forum


urlpatterns = [
    path('admin/', admin.site.urls),
    #@W_Farmer
    # User authentication paths
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('forum/', include('Forum.urls'), name='Forum'), #@W_Farmer Forum url
    path('boards/', include('IdeaBoards.urls')),
    path('profile/', include('ProfileApp.urls')),
    path('notifications/mark_as_read/<int:notification_id>/', forum.mark_notification_as_read, name='mark_notification_as_read'), #@W_Farmer, Global notification mark as read

    path('' , views.home, name='home'),

    ]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
