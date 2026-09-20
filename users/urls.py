from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/added/', views.added, name='added'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('account/edit/', views.edit, name='edit'),
    path('account/edit/preview/', views.edit_preview, name='edit_preview'),
    path('users/', views.user_list, name='user_list'),
    path('users/edit/', views.edit_user, name='edit_user'),
    path('users/admin-review/', views.admin_review, name='admin_review'),
    path('reviews/', views.review, name='review'),
    path('reviews/new/', views.comment, name='comment'),
    path('reviews/added/', views.comment_added, name='comment_added'),
    path('reviews/edit/', views.edit_review, name='edit_review'),
    path('reviews/edited/', views.comment_edited, name='comment_edited'),
    path('reviews/delete/', views.delete_comment, name='delete'),
]
