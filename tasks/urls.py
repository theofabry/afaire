from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from tasks import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskList.as_view(), name='list'),
    path('<int:task_pk>', views.TaskDetail.as_view(), name='detail'),
    path('tags/', views.TaskTagList.as_view(), name='tags-list'),
    path('tags/<task_tag_pk>/', views.TaskTagDetail.as_view(), name='tags-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
