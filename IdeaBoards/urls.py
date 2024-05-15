from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.IdeaBoards_Home, name='IdeaBoards_Home'),
    path('<int:id>/', views.IdeaBoard_Detail, name='IdeaBoard_Detail'),
    path('<int:id>/comment/', views.create_comment, name='create_board_comment'),
    path('boards/<int:comment_id>/delete_board_comment/', views.delete_comment, name='delete_board_comment'),
    path('boards/<int:comment_id>/edit_comment/', views.edit_comment, name='edit_board_comment'),
    path('boards/<int:comment_id>/like_board_comment/', views.like_comment, name='like_board_comment'),
    path('thread/<int:thread_id>/reply-to-comment/<int:parent_comment_id>/', views.reply_to_comment, name='reply_to_board_comment'),
    #path('<int:id>/<int:comment_id>/', views.IdeaBoard_Detail, name='board_detail_comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

