# forum/views.py
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Notification, Thread, Page, Comment
from .forms import ThreadForm, PageForm, CommentForm
from django.db.models import Count
from django.db.models import Max, F
from django.utils import timezone


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

    # Get the time and username of the latest comment for each thread
    for thread in threads:
        latest_comment = Comment.objects.filter(thread=thread).order_by('-created_at').first()
        if latest_comment:
            thread.latest_comment_time = latest_comment.created_at
            thread.latest_comment_username = latest_comment.user.username
        else:
            thread.latest_comment_time = None
            thread.latest_comment_username = "No comments"

    # Now order threads by the latest_comment_time in descending order
    latest_threads = sorted(threads, key=lambda x: (x.latest_comment_time is not None, x.latest_comment_time), reverse=True)[:5]

    # Get top threads based on comment count
    top_threads = Thread.objects.annotate(num_comments=Count('comment')).order_by('-num_comments')[:5]
    
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
    
def create_comment(request, thread_id, parent_comment_id=None):
    thread = get_object_or_404(Thread, id=thread_id)
    parent_comment = None
    if parent_comment_id:
        parent_comment = get_object_or_404(Comment, id=parent_comment_id, thread=thread)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.user = request.user
            comment.parent = parent_comment  # Set the parent comment
            comment.save()
            
            return redirect('thread_detail', thread_id=thread_id)
            # Redirect or handle as needed
    # Form rendering and other view logic
    return render(request, 'create_comment.html', {'form': form, 'thread': thread, 'parent_comment': parent_comment})





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



# Here we want to be able to edit a comment, either by deleating it, or by changing the content, and the user HAS to be the one logged in, or a superuser
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    # Check if the user is the author of the comment or a superuser
    if request.user != comment.user and not request.user.is_superuser:
        # Throw an error, they are not authorized to do this
        return HttpResponseForbidden("You are not authorized to edit this comment.")
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            #update the last edited time
            comment.last_edited = timezone.now()
            form.save()
            return redirect('thread_detail', thread_id=comment.thread.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})

# To make it easier on myself, I have a seperate view for deleting a comment
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    # Check if the user is the author of the comment or a superuser
    if request.user != comment.user and not request.user.is_superuser:
        # Throw an error, they are not authorized to do this
        return HttpResponseForbidden("You are not authorized to delete this comment.")
    comment.delete()
    return redirect('thread_detail', thread_id=comment.thread.id)


def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        # No notification on unlike
    else:
        comment.likes.add(request.user)
        # Create notification for like
        if comment.user != request.user:  # Don't notify if liking their own comment
            Notification.objects.create(
                notification_type=Notification.LIKE,
                to_user=comment.user,
                from_user=request.user,
                thread=comment.thread,
                comment=comment,
                is_read=False
            )
    return redirect('thread_detail', thread_id=comment.thread.id)



@login_required
def notifications_page(request):
    user_notifications = request.user.notifications.all().order_by('-date')
    
    # Mark all notifications as read
    user_notifications.update(is_read=True)
    
    return render(request, 'notifications_page.html', {'notifications': user_notifications})


# Making it easier on myself by making a seperate view for replies to comments
def reply_to_comment(request, thread_id, parent_comment_id):
    thread = get_object_or_404(Thread, id=thread_id)
    parent_comment = get_object_or_404(Comment, id=parent_comment_id, thread=thread)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.user = request.user
            comment.parent = parent_comment  # Set the parent comment
            comment.save()
            
            return redirect('thread_detail', thread_id=thread_id)
            # Redirect or handle as needed
    # Form rendering and other view logic
    return render(request, 'reply_to_comment.html', {'form': form, 'thread': thread, 'parent_comment': parent_comment})