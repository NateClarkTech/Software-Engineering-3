from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout


from django.shortcuts import render, redirect, get_object_or_404

# The primary view for the profile, this is for the current user
@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect or show success message
            return redirect('Profile:profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    
    context = {'form': form, 'profile': profile}
    return render(request, 'profiles/profile.html', context)

# Much the same as the profile view, this is to view other users profiles
def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    context = {
        'user_profile': user,
        'profile': profile
    }
    return render(request, 'profiles/profile.html', context)

# Profile searching view
def search_profiles(request):
    form = ProfileSearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = ProfileSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Profile.objects.filter(
                user__username__icontains=query
            )

    return render(request, 'profiles/profile_search.html', {
        'form': form,
        'query': query,
        'results': results
    })
    
    
    


# Using Djangos registration form, and letting us registering the new user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # Create profile for the new user
            login(request, user)  # Automatically log in the user after registration
            return redirect('calendar')  # Redirect to the desired URL after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('calendar')

# A view to allow the user to edit the profile
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect or show success message
            return redirect('Profile:profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    
    context = {'form': form, 'profile': profile}
    return render(request, 'profiles/edit_profile.html', context)