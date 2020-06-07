from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from tasks.factories import TaskFactory
from tasks.models import TaskTag, Task
from users.factories import TokenFactory
from users.models import User


class TaskTagListTests(APITestCase):
    def setUp(self) -> None:
        self.token: Token = TokenFactory()
        self.user: User = self.token.user

    def test_get_tags(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/tasks/tags/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        tag: TaskTag = TaskTag.objects.create(user=self.user, name='new tag')

        response = self.client.get('/tasks/tags/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'new tag')

        task: Task = TaskFactory(user=self.user)
        task.tags.add(tag)
        task.save()

        response = self.client.get('/tasks/tags/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'new tag')
        self.assertEqual(len(response.json()[0]['task_set']), 1)
        self.assertTrue(task.pk in response.json()[0]['task_set'])

        task = TaskFactory(user=self.user)
        task.tags.add(tag)
        task.save()

        response = self.client.get('/tasks/tags/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(len(response.json()[0]['task_set']), 2)

    def test_get_tags_not_logged_in(self):
        response = self.client.get('/tasks/tags/')

        self.assertEqual(response.status_code, 401)
