import datetime

from django.db import models

from users.models import User


class TaskManager(models.Manager):
    def get_tasks_by_date(self, user: User):
        tasks = self.filter(user=user, due_date__gte=datetime.date.today())
        tasks_by_date = {}

        for current_date in [datetime.date.today() + datetime.timedelta(n) for n in range(30)]:
            tasks_by_date[current_date.strftime('%Y-%m-%d')] = []

        for task in tasks:
            tasks_by_date[task.due_date.strftime('%Y-%m-%d')].append({
                'id': task.pk,
                'content': task.content,
                'due_date': task.due_date,
                'status': task.status,
            })

        return tasks_by_date


class Task(models.Model):
    STATUS_DONE = 0
    STATUS_NOT_DONE_BEYOND_CONTROL = 1
    STATUS_NOT_DONE_LAZINESS = 2
    STATUS_FAILED = 3
    STATUS_DONE_MULTIPLE_STEPS = 4

    STATUS_CHOICES = (
        (STATUS_DONE, 'Réalisé'),
        (STATUS_NOT_DONE_BEYOND_CONTROL, 'Non réalisé, indépendamment de ma volonté'),
        (STATUS_NOT_DONE_LAZINESS, 'Non réalisé, manque de temps/flemme'),
        (STATUS_FAILED, 'Echoué/abandonné'),
        (STATUS_DONE_MULTIPLE_STEPS, 'Réalisé après de nombreuses étapes'),
    )

    content = models.TextField()
    due_date = models.DateField()
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = TaskManager()
