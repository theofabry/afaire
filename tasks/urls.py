from django.urls import path

from tasks import views

app_name = 'tasks'

urlpatterns = [
    path('', views.tasks_list, name='list'),
    path('<int:task_pk>', views.task_details, name='details'),
    path('ajouter', views.task_add, name='add'),
    path('<int:task_pk>/supprimer', views.task_delete, name='delete'),
]
