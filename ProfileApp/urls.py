from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
# Got a lot of help from herehttps://www.reddit.com/r/django/comments/hfh1qc/namespace_is_not_a_registered_namespace/
# https://forum.djangoproject.com/t/django-urls-exceptions-noreversematch-is-not-a-registered-namespace/1876/2
#https://forum.djangoproject.com/t/redirect-to-a-different-app/9086
# And GPT helped me fix everything

app_name = 'ProfileApp'
#@W_Farmer
# Here we have the urls for the profile app
urlpatterns = [

    path('', views.profile, name='profile'),  # For the logged-in user's profile
    path('profile/', views.profile, name='profile'),  # For the logged-in user's profile
    path('profile/<str:username>/', views.profile, name='public_profile'),  # For viewing other users' profiles
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('search/', views.search_profiles, name='search_profiles'),

    # link the media files
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

