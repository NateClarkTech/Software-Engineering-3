# forum/views.py
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Thread, Page, Comment
from .forms import ThreadForm, PageForm, CommentForm
from django.db.models import Count
from django.db.models import Max, F


def thread_list(request, page_id):
    page = Page.objects.get(pk=page_id)
    threads = Thread.objects.filter(page=page).distinct()

    for thread in threads:
        latest_comment = Comment.objects.filter(thread=thread).order_by('-created_at').first()
        if latest_comment:
            thread.latest_comment_time = latest_comment.created_at
            thread.latest_comment_username = latest_comment.user.username
        else:
            thread.latest_comment_time = None
            thread.latest_comment_username = "No comments"
            
    # now order them
    threads = sorted(threads, key=lambda x: x.latest_comment_time, reverse=True)
    return render(request, 'thread_list.html', {'threads': threads, 'page': page})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    comments = Comment.objects.filter(thread=thread)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.user = request.user  # Assuming you're using user authentication
            comment.save()
            return redirect('thread_detail', thread_id=thread_id)
    else:
        form = CommentForm()
    return render(request, 'thread_details.html', {'thread': thread, 'comments': comments, 'form': form})



# forum/views.py
from django.db.models import Max, F
# ... (the rest of your imports)

def forum_home(request):
    pages = Page.objects.all()
    
    # Get all threads without distinct, as we want to manually add latest comment information
    threads = Thread.objects.all()

    # Enrich each thread with the latest comment info
    for thread in threads:
        latest_comment = Comment.objects.filter(thread=thread).order_by('-created_at').first()
        if latest_comment:
            thread.latest_comment_time = latest_comment.created_at
            thread.latest_comment_username = latest_comment.user.username
        else:
            thread.latest_comment_time = None
            thread.latest_comment_username = "No comments"

    # Now order threads by the latest_comment_time in descending order
    # Threads without comments will be at the end of the list
    latest_threads = sorted(threads, key=lambda x: (x.latest_comment_time is not None, x.latest_comment_time), reverse=True)[:10]

    # Get top threads based on comment count
    top_threads = Thread.objects.annotate(num_comments=Count('comment')).order_by('-num_comments')[:10]
    
    return render(request, 'forum_home.html', {
        'pages': pages,
        'latest_threads': latest_threads,
        'top_threads': top_threads
    })


@login_required
def create_thread(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    if request.method == 'POST':
        thread_form = ThreadForm(request.POST)
        comment_form = CommentForm(request.POST)
        if thread_form.is_valid() and comment_form.is_valid():
            thread = thread_form.save(commit=False)
            thread.page = page
            thread.save()  # Save the thread to get a valid ID
            comment = comment_form.save(commit=False)
            comment.thread = thread  # Associate the comment with the newly created thread
            comment.user = request.user  # Assign the logged-in user as the author of the comment
            comment.save()  # Save the initial comment
            return redirect('thread_detail', thread_id=thread.id)
    else:
        thread_form = ThreadForm()
        comment_form = CommentForm()
    
    return render(request, 'create_thread.html', {
        'thread_form': thread_form,
        'comment_form': comment_form,
        'page': page
    })
    
    
@login_required
def create_comment(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        form = CommentForm()

    # If this view is called with a GET request, just redirect to the thread detail page
    return redirect('thread_detail', thread_id=thread_id)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_page(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forum_home')
    else:
        form = PageForm()
    return render(request, 'create_page.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def modify_page(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    if request.method == 'POST':
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            return redirect('forum_home')
    else:
        form = PageForm(instance=page)
    return render(request, 'modify_page.html', {'form': form, 'page': page})
