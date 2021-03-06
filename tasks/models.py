import datetime
from collections import defaultdict

from django.db import models

from afaire import settings
from users.models import User


class TaskManager(models.Manager):
    def get_close_tasks(self, user: User):
        start_date = datetime.date.today() - datetime.timedelta(days=settings.TASKS_PAST_DAYS)
        end_date = datetime.date.today() + datetime.timedelta(days=settings.TASKS_FUTURE_DAYS)

        return self.filter(user=user, due_date__gte=start_date, due_date__lte=end_date)

    def get_tasks_by_date(self, user: User) -> []:
        tasks_by_date = []

        for i in range(-settings.TASKS_PAST_DAYS, settings.TASKS_FUTURE_DAYS):
            current_date = datetime.date.today() + datetime.timedelta(days=i)

            tasks_by_date.append({
                'date': current_date,
                'tasks': self.filter(user=user, due_date=current_date).order_by('content'),
            })

        return tasks_by_date

    def get_all_tasks_grouped_by_date(self, user: User):
        tasks = self.filter(user=user).order_by('due_date', 'content')
        tasks_by_date = defaultdict(list)

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
    STATUS_TODO = 5
    STATUS_PROGRESSED_NOT_DONE = 6
    STATUS_DONE_NOT_PLANNED = 7

    STATUS_CHOICES = (
        (STATUS_DONE, 'Réalisé'),
        (STATUS_NOT_DONE_BEYOND_CONTROL, 'Non réalisé, indépendamment de ma volonté'),
        (STATUS_NOT_DONE_LAZINESS, 'Non réalisé, manque de temps/flemme'),
        (STATUS_FAILED, 'Echoué/abandonné'),
        (STATUS_DONE_MULTIPLE_STEPS, 'Réalisé après de nombreuses étapes'),
        (STATUS_TODO, 'A faire'),
        (STATUS_PROGRESSED_NOT_DONE, 'Avancé mais pas terminé'),
        (STATUS_DONE_NOT_PLANNED, 'Fait sans avoir été prévu'),
    )

    content = models.TextField()
    due_date = models.DateField()
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS_TODO)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = TaskManager()

    def __str__(self):
        return 'Tâche de {}'.format(self.user.username)
