from django.urls import path

from tasks import views

app_name = 'tasks'

urlpatterns = [
    path('', views.tasks_list, name='list'),
]
