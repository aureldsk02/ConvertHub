"""
URLs pour l'application users
"""
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('stats/', views.UserStatsView.as_view(), name='stats'),
]
