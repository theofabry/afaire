from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from tasks.api import views

app_name = 'tasks-api'

urlpatterns = [
    path('', views.TaskList.as_view(), name='list'),
    path('<int:task_pk>', views.TaskDetail.as_view(), name='details'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
