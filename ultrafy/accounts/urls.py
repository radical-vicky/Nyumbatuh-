from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('edit/', views.profile_edit, name='profile_edit'),
]
