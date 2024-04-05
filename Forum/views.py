# forum/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Thread, Page, Comment
from .forms import ThreadForm, PageForm, CommentForm

def thread_list(request, page_id):
    page = Page.objects.get(pk=page_id)
    threads = Thread.objects.filter(page=page)
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


def forum_home(request):
    pages = Page.objects.all()
    return render(request, 'forum_home.html', {'pages': pages})

@login_required
def create_thread(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.page = page
            thread.save()
            return redirect('thread_detail', thread_id=thread.id)
    else:
        form = ThreadForm()
    return render(request, 'create_thread.html', {'form': form, 'page': page})

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
