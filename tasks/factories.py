from datetime import date

from factory import DjangoModelFactory, Sequence, LazyFunction, SubFactory

from tasks.models import Task, TaskTag
from users.factories import UserFactory


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task

    content = Sequence('content{0}'.format)
    due_date = LazyFunction(date.today)
    user = SubFactory(UserFactory)


class TaskTagFactory(DjangoModelFactory):
    class Meta:
        model = TaskTag

    name = Sequence('tag{0}'.format)
    user = SubFactory(UserFactory)
