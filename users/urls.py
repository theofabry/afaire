from django.urls import path
from django.contrib.auth import views as auth_views

from users import views

app_name = 'users'

urlpatterns = [
    path('inscription', views.register, name='register'),
    path('connexion', views.LoginView.as_view(), name='login'),
    path('deconnexion', auth_views.LogoutView.as_view(), name='logout'),
    path('mes-donnees', views.my_data, name='my-data'),
    path('mes-donnees/telecharger', views.download_my_data, name='my-data-download'),
    path('mes-infos', views.my_information, name='my-information'),
    path('e-mail', views.update_email, name='update-email'),
    path('mot-de-passe', views.update_password, name='update-password'),
]
