
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
# Got a lot of help from herehttps://www.reddit.com/r/django/comments/hfh1qc/namespace_is_not_a_registered_namespace/
# https://forum.djangoproject.com/t/django-urls-exceptions-noreversematch-is-not-a-registered-namespace/1876/2
#https://forum.djangoproject.com/t/redirect-to-a-different-app/9086
# And GPT helped me fix everything

app_name = 'Profile'

# Here we have the urls for the profile app
urlpatterns = [

    path('profile/', views.profile, name='profile'),  # For the logged-in user's profile
    path('profile/<str:username>/', views.public_profile, name='public_profile'),  # For viewing other users' profiles
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('search/', views.search_profiles, name='search_profiles'),

    
        # Login/logout stuff
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    
    # link the media files
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

