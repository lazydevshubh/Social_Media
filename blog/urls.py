from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(),name="blog-home"),
    path('post/<int:pk>/', views.PostDetailView.as_view(),name="post-details"),
    path('post/update/<int:pk>/', views.PostUpdateView.as_view(),name="post-update"),
    path('post/like/', views.PostLike,name="post-like"),
    path('post/delete_comment/', views.Delete_comment,name="delete-comment"),
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(),name="post-delete"),
    path('post/new/', views.PostCreateView.as_view(),name="post-create"),
    path('about/', views.about,name="blog-about"),
]