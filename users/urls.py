from django.urls import path
from django.contrib.auth import views as auth_views

from users import views

app_name = 'users'

urlpatterns = [
    path('inscription', views.register, name='register'),
    path('connexion', views.LoginView.as_view(), name='login'),
    path('deconnexion', auth_views.LogoutView.as_view(), name='logout'),
]
