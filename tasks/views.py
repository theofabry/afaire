from typing import Optional

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from tasks.forms import AddTaskForm, EditTaskForm, DeleteTaskForm
from tasks.models import Task


@login_required
def tasks_list(request: WSGIRequest):
    tasks_by_date: [Task] = Task.objects.get_tasks_by_date(request.user)

    return render(request, 'tasks/tasks.html', {
        'active_menu': 'tasks',
        'tasks_by_date': tasks_by_date,
    })


@login_required
def task_details(request: WSGIRequest, task_pk: int):
    task: Task = get_object_or_404(Task, pk=task_pk)

    if task.user != request.user:
        messages.add_message(request, messages.ERROR, 'Vous n\'êtes pas autorisé à consulter cette tâche')

        return redirect(reverse('tasks:list'))

    form = EditTaskForm(instance=task)

    if request.method == 'POST':
        form = EditTaskForm(instance=task, data=request.POST)

        if form.is_valid():
            form.save()

            return redirect(reverse('tasks:list'))

    return render(request, 'tasks/task_details.html', {
        'active_menu': 'tasks',
        'task': task,
        'form': form,
    })


@login_required
def task_add(request: WSGIRequest):
    due_date: Optional[str] = request.GET.get('pour_le')

    form = AddTaskForm(initial={'due_date': due_date})

    if request.method == 'POST':
        form = AddTaskForm(data=request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.save()

            return redirect(reverse('tasks:list'))

    return render(request, 'tasks/task_add.html', {
        'active_menu': 'tasks',
        'form': form,
    })


@require_POST
def task_delete(request: WSGIRequest, task_pk: int):
    task: Task = get_object_or_404(Task, pk=task_pk)

    if task.user != request.user:
        messages.add_message(request, messages.ERROR, 'Vous n\'êtes pas autorisé à consulter cette tâche')

        return redirect(reverse('tasks:list'))

    if request.method == 'POST':
        form = DeleteTaskForm(data=request.POST)

        if form.is_valid():
            task.delete()

            return redirect(reverse('tasks:list'))

        return redirect(reverse('tasks:details', kwargs={'task_pk': task.pk}))
