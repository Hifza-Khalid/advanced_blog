from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/create/', views.post_create, name='post_create'),  # This should come BEFORE the slug pattern
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),  # This should be LAST
    path('category/<slug:slug>/', views.posts_by_category, name='posts_by_category'),
    path('tag/<slug:slug>/', views.posts_by_tag, name='posts_by_tag'),
    path('dashboard/', views.dashboard, name='dashboard'),
]