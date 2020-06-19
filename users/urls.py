from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.register,name="register"),
    path('profile/', views.profile,name="profile"),
    path('message/<int:id>/', views.messages,name="messages"),
    path('<str:username>/', views.OtherPostListView.as_view(),name="other-user"),
    
    
]