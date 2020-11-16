from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from pages import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='index'),
    path('presentation', views.presentation, name='presentation'),
    path('mentions-legales', views.mentions, name='mentions-legales'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
