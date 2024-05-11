from django.shortcuts import render
from .models import *
from .forms import *
from Forum.models import Thread, Comment, Notification
from Forum.forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.core.paginator import Paginator



from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import EmptyPage , PageNotAnInteger, Paginator

# View for a profile page, which will functino for both the current user, or a specefic user
@login_required 
def profile(request, username=None): #@W_Farmer
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    # Get or create the profile for the user
    profile, created = Profile.objects.get_or_create(user=user)
    comments_query = ProfileComment.objects.filter(profile=profile).order_by('-created_at')
    threads_query = Thread.objects.filter(original_poster=user).order_by('-created_at')
    user_comments_query = Comment.objects.filter(user=user).order_by('-created_at')
    
    # Count the users statistics
    thread_count = threads_query.count()
    comment_count = user_comments_query.count()
    
    #TODO Get the number of likes the user has received and given 
    likes_received = 0
    likes_given = 0
    

    # Separate pagination for threads, user comments, and profile comments
    threads_page = request.GET.get('threads_page', 1)
    user_comments_page = request.GET.get('user_comments_page', 1)
    profile_comments_page = request.GET.get('profile_comments_page', 1)

    threads_paginator = Paginator(threads_query, 5)
    user_comments_paginator = Paginator(user_comments_query, 5)
    profile_comments_paginator = Paginator(comments_query, 5)

    # Try to get the page number, if not set to 1
    try:
        threads = threads_paginator.page(threads_page)
        user_comments = user_comments_paginator.page(user_comments_page)
        profile_comments = profile_comments_paginator.page(profile_comments_page)
    except PageNotAnInteger:
        threads = threads_paginator.page(1)
        user_comments = user_comments_paginator.page(1)
        profile_comments = profile_comments_paginator.page(1)
    except EmptyPage:
        threads = threads_paginator.page(threads_paginator.num_pages)
        user_comments = user_comments_paginator.page(user_comments_paginator.num_pages)
        profile_comments = profile_comments_paginator.page(profile_comments_paginator.num_pages)
    # Allow the user to post a comment on the profile
    comment_form = ProfileCommentForm(request.POST or None)
    
    if request.method == 'POST' and comment_form.is_valid():
        new_comment = ProfileComment.objects.create(
            profile=profile,
            user=request.user,
            content=comment_form.cleaned_data['content']
        )
        return redirect('ProfileApp:public_profile', username=user.username)

    context = {
        'user_profile': user,
        'profile': profile,
        'threads': threads,
        'user_comments': user_comments,
        'comments': profile_comments,
        'comment_form': comment_form,
        'thread_count': thread_count,
        'comment_count': comment_count,
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

# A view to allow the user to edit the profile
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect or show success message
            return redirect('ProfileApp:profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    
    context = {'form': form, 'profile': profile}
    return render(request, 'profiles/edit_profile.html', context)