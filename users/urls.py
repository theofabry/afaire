from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns

from users import views

app_name = 'users'

urlpatterns = [
    path('', views.users_list, name='list'),
    path('login/', obtain_auth_token, name='login'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
