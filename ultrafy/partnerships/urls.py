from django.urls import path
from . import views

urlpatterns = [
    path('', views.partnership_landing, name='partnership_landing'),
    path('apply/', views.partnership_apply, name='partnership_apply'),
    path('status/', views.partnership_status, name='partnership_status'),
]
