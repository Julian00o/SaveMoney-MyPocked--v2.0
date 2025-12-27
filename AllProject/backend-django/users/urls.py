from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),  # Наш кастомный login
    path('user/', views.user_info, name='user_info'),
    path('profile/', views.profile, name='profile'),
    path('', views.api_root, name='api_root'),
]
