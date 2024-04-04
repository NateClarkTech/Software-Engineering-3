from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_home, name='forum_home'),
    path('page/create_thread/<int:page_id>', views.create_thread, name='create_thread'),
    path('create_page/', views.create_page, name='create_page'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('thread_list/<int:page_id>/', views.thread_list, name='thread_list'),

    # Add other URLs
]
