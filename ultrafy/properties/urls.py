from django.urls import path
from . import views
from accounts.views import dashboard as accounts_dashboard

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/new/', views.property_create, name='property_create'),
    path('properties/mine/', views.my_properties, name='my_properties'),
    path('properties/<slug:slug>/', views.property_detail, name='property_detail'),
    path('properties/<slug:slug>/delete/', views.property_delete, name='property_delete'),
    path('dashboard/', accounts_dashboard, name='profile_dashboard'),
]
