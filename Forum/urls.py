from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_home, name='forum_home'),
    path('page/create_thread/<int:page_id>', views.create_thread, name='create_thread'),
    path('create_page/', views.create_page, name='create_page'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('thread_list/<int:page_id>/', views.thread_list, name='thread_list'),
    path('thread/<int:thread_id>/comment/', views.create_comment, name='create_comment'),
    path('thread/<int:comment_id>/edit_comment/', views.edit_comment, name='edit_comment'),
    path('thread/<int:comment_id>/delete_comment/', views.delete_comment, name='delete_comment'),
    path('thread/<int:comment_id>/like_comment/', views.like_comment, name='like_comment'),
    path('notifications/', views.notifications_page, name='notifications'),
    path('thread/<int:thread_id>/reply-to-comment/<int:parent_comment_id>/', views.reply_to_comment, name='reply_to_comment'),

    # Add other URLs
]
