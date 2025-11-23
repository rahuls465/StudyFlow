from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/register/', views.api_register),
    path('api/login/', views.api_login),
    path('api/logout/', views.api_logout),
    path('api/session/', views.api_session),
    path('api/progress/save/', views.api_save_progress),
    path('api/progress/get/', views.api_get_progress),
]
