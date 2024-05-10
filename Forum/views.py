from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.db.models import Count, OuterRef, Subquery, Max, F
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import JsonResponse

# Custom Imports from the Forum App
from .models import Notification, Thread, Page, Comment
from .forms import ThreadForm, PageForm, CommentForm
from .utils import convert_media_links_to_embed, clean_html

# Custom Imports from the Profile App
from ProfileApp.models import Profile



#@W_Farmer
# This view represents a list of threads, it can take in a page_id, and will display all threads on that page
def thread_list(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    threads = Thread.objects.filter(page=page).distinct()

    for thread in threads:
        # This does produce an error, but it is dynamically adding these fields to the thread, so it works, but I havent added it to the mo
        latest_comment = Comment.objects.filter(thread=thread).order_by('-created_at').first()
        if latest_comment:
            thread.latest_comment_time = latest_comment.created_at
            thread.latest_comment_username = latest_comment.user.username
        else:
            thread.latest_comment_time = None
            thread.latest_comment_username = "No comments"
            
    # Order the threads by the latest comment time in descending order
    threads = sorted(threads, key=lambda x: x.latest_comment_time, reverse=True)
    
    # Pagination For the threads, should it be needed 
    paginator = Paginator(threads, 10)  # Shows 10 threads per page
    page_number = request.GET.get('page')
    try:
        threads = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        threads = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        threads = paginator.page(paginator.num_pages)

    return render(request, 'thread_list.html', {'threads': threads, 'page': page})

#@W_Farmer
# This view is a detailed view of a specefic view, It can take in a thread_id, and a comment_id, and will display the thread, and the comments on that thread
def thread_detail(request, thread_id, comment_id=None):
    thread = get_object_or_404(Thread, id=thread_id)
    # Sort comments by created_at date and that belong to said thread
    comments_list = Comment.objects.filter(thread=thread).order_by('created_at')
    
    # Integer to store the number of comments we want to display per page
    per_page = 15
    paginator = Paginator(comments_list, per_page)

    # Default to page 1 if no specific comment is targeted
    if comment_id:
        comment = Comment.objects.get(id=comment_id)
        try:
            # Get the list of IDs to find the index, then determine page number
            comment_ids = comments_list.values_list('id', flat=True)
            comment_index = list(comment_ids).index(comment.id)
            page_number = comment_index // per_page + 1
        except (ValueError, Comment.DoesNotExist):
            page_number = 1
    else:
        page_number = request.GET.get('page', 1)

    # Get the comments for the current page if we have a page number, otherwise default to page 1
    try:
        comments = paginator.page(page_number)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    return render(request, 'thread_details.html', {
        'thread': thread,
        'comments': comments,
        'form': CommentForm(),
    })


#@W_Farmer
# # Utility view to mark a specific notification as read
@require_POST
@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, to_user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})


#@W_Farmer
# The home page of the forum, This will display the top 5 most recent threads, the top 5 most commented threads, and the top 10 most recent commenters
def forum_home(request):
    pages = Page.objects.all()
    
    # Get all threads without distinct, as we want to manually add latest comment information
    threads = Thread.objects.all()
    
    # Subquery to fetch the most recent comment date per user
    latest_comments = Comment.objects.filter(user=OuterRef('user')).order_by('-created_at')
    
    # Fetch profiles with latest comment dates, ordered by those dates
    profiles_with_latest_comment_dates = Profile.objects.select_related('user').annotate(
        latest_comment_date=Subquery(latest_comments.values('created_at')[:1])
    ).filter(
        latest_comment_date__isnull=False  # Ensure the profile has at least one comment
    ).order_by('-latest_comment_date')[:10]  # Get the top 10
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
        'top_threads': top_threads,
        'recent_commenter_profiles': profiles_with_latest_comment_dates,
    })

#@W_Farmer
# View to allow a user to create a new thread, it will take in a page_id, and will create a new thread on that page
@login_required
def create_thread(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    
    if request.method == 'POST':
        thread_form = ThreadForm(request.POST)
        comment_form = CommentForm(request.POST)
        if thread_form.is_valid() and comment_form.is_valid():
            
            thread = thread_form.save(commit=False)
            
            comment_content = comment_form.cleaned_data['content']
            # Convert links to embeds and sanitize
            comment_content = convert_media_links_to_embed(comment_content)
            comment_content = clean_html(comment_content)


            comment = comment_form.save(commit=False)
            # Set the processed content with YouTube embeds
            comment.content = comment_content 


            # Associate the new thread with its page, the logged-in user as the original poster, and the initial comment
            thread.page = page
            thread.original_poster = request.user
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
    
#@W_Farmer
# This view will allow the user to create a new comment on the forum. 
@login_required
def create_comment(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment_content = form.cleaned_data['content']
        # Convert YouTube links to embeds

        # Convert links to embeds and sanitize
        comment_content = convert_media_links_to_embed(comment_content)
        comment_content = clean_html(comment_content)  # Clean the HTML

        # Create the comment object
        comment = form.save(commit=False)
        comment.content = comment_content  # Set the processed content with YouTube embeds
        # Associate the comment with the thread and the logged-in user
        comment.user = request.user
        comment.thread = thread
        comment.save()
        
        # Update the latest comment info for the thread
        thread.latest_comment_time = comment.created_at
        thread.latest_comment_username = comment.user.username
        thread.save()

        # Create a set to collect unique recipients
        recipients = set(thread.subscribers.all())  # Start with all subscribers

        # Always add the original poster 
        if thread.original_poster != request.user:
            recipients.add(thread.original_poster)

        # Remove the comment author to prevent them from receiving their own notification
        recipients.discard(request.user)

        # Create notifications for each unique recipient
        for recipient in recipients:
            Notification.objects.create(
                notification_type=Notification.COMMENT,
                to_user=recipient,
                from_user=request.user,
                thread=thread,
                comment=comment
            )
            
        return redirect(reverse('thread_detail_comment', args=[thread.id, comment.id]))
    else:
        # Handle errors or redirect
        return render(request, 'thread_detail.html', {'form': form, 'thread': thread})


#@W_Farmer
# This is a view created to allow for an admin to create a new page on the forum
def create_page(request):
    # if the user isnt a superuser return forbidden error
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to create a new page.")
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forum_home')
    else:
        form = PageForm()
    return render(request, 'create_page.html', {'form': form})

#@W_Farmer
# This is a view to allow an admin to modify a page should they wish too. It is not currently enabled However it will exist for the future deployments. 
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
    return render(request, 'create_page.html', {'form': form, 'page': page})


#@W_Farmer
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

#@W_Farmer
# This is a view to allow the user to delete a comment, they have to be the author of the comment, or a superuser
def delete_comment(request, comment_id):
    # Add a check to see uf the user is authentacated at all
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You are not authorized to delete this comment.")
    
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if the user is the author of the comment or a superuser
    if request.user != comment.user and not request.user.is_superuser:
        # Throw an error, they are not authorized to do this
        return HttpResponseForbidden("You are not authorized to delete this comment.")
    comment.delete()
    return redirect('thread_detail', thread_id=comment.thread.id)

#@W_Farmer
# This is a view that will allow a user to like a comment, or unlike said comment
def like_comment(request, comment_id):
    # Some checks to make sure that the user cannot like their comment, even by messing with the urls

    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user and not request.user.is_superuser:
        # Throw an error, they are not authorized to do this
        return HttpResponseForbidden("You shouldn't be seeing this. bad. no liking this comment.")
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        # No notification on unlike
    else:
        comment.likes.add(request.user)
        # Create notification for like
        Notification.objects.create(
            notification_type=Notification.LIKE,
            to_user=comment.user,
            from_user=request.user,
            thread=comment.thread,
            comment=comment,
            is_read=False
        )
    return redirect('thread_detail', thread_id=comment.thread.id)


#@W_Farmer
# This view will display all the notifications for the user, and mark them as read at the same time. 
@login_required
def notifications_page(request):
    user_notifications_list = request.user.notifications.all().order_by('-date')
    paginator = Paginator(user_notifications_list, 20)  # Show 20 notifications per page
    # mark all notifications as read
    user_notifications_list.update(is_read=True)

    page_number = request.GET.get('page')
    user_notifications = paginator.get_page(page_number)
    
    return render(request, 'notifications_page.html', {'notifications': user_notifications})

#@W_Farmer
# This is a seperate view to handle the creation of a reply to a comment, it will take in a thread_id, and a parent_comment_id, and will create a reply to that comment
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
            
            # Update the latest comment info for the thread
            thread.latest_comment_time = comment.created_at
            thread.latest_comment_username = comment.user.username
            thread.save()
            
            return redirect('thread_detail_comment' , thread_id=thread.id, comment_id=comment.id)
    return render(request, 'reply_to_comment.html', {'form': form, 'thread': thread, 'parent_comment': parent_comment})

#@W_Farmer
# Views to handle subscribing and unsubscribing from threads
#TODO: combine these into one "toggle" view later. 
@login_required
def subscribe_to_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    thread.subscribers.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def unsubscribe_from_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    thread.subscribers.remove(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
