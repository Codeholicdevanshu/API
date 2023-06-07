from django.urls import path
from app import views
from .views import *

urlpatterns = [
    path('register',views.register,name='register'),
    path('api/register', RegisterView.as_view(),name='register'),
    path('api/login',LoginAPI.as_view(),name='login'),
    path('login',login,name='login'),
    path('base',views.base,name='base')
]