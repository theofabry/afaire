from django.urls import path, include

urlpatterns = [
    path('tasks/', include('tasks.api.urls')),
    path('users/', include('users.api.urls')),
]
