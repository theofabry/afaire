from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from tasks.models import Task


@login_required
def tasks_list(request: WSGIRequest):
    tasks_by_date: [Task] = Task.objects.get_tasks_by_date(request.user)

    return render(request, 'tasks/tasks.html', {
        'active_menu': 'tasks',
        'tasks_by_date': tasks_by_date,
    })
