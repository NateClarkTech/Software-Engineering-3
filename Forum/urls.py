from django.urls import path
from . import views

urlpatterns = [
    # Forum Home page
    path('', views.forum_home, name='forum_home'),
    # Create threads on a page
    path('page/create_thread/<int:page_id>', views.create_thread, name='create_thread'),
    # Admin page to create pages
    path('create_page/', views.create_page, name='create_page'),
    
    # Thread detail page, Two versions of the URL, one with a comment_id to page to a specific comment
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('thread/<int:thread_id>/<int:comment_id>/', views.thread_detail, name='thread_detail_comment'),

    # List of threads belonging to a page
    path('thread_list/<int:page_id>/', views.thread_list, name='thread_list'),
    
    # Create, edit, delete, like, comments
    path('thread/<int:thread_id>/comment/', views.create_comment, name='create_comment'),
    path('thread/<int:comment_id>/edit_comment/', views.edit_comment, name='edit_comment'),
    path('thread/<int:comment_id>/delete_comment/', views.delete_comment, name='delete_comment'),
    path('thread/<int:comment_id>/like_comment/', views.like_comment, name='like_comment'),
    # Reply to comments
    path('thread/<int:thread_id>/reply-to-comment/<int:parent_comment_id>/', views.reply_to_comment, name='reply_to_comment'),

    
    # Notifications page
    path('notifications/', views.notifications_page, name='notifications'),
    
    # Subscribe and unsubscribe to threads
    path('thread/<int:thread_id>/subscribe/', views.subscribe_to_thread, name='subscribe_to_thread'),
    path('thread/<int:thread_id>/unsubscribe/', views.unsubscribe_from_thread, name='unsubscribe_from_thread'),

]
