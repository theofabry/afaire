from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APITransactionTestCase

from tasks.factories import TaskFactory, TaskTagFactory
from tasks.models import TaskTag, Task
from users.factories import TokenFactory
from users.models import User


class TaskDetailTests(APITestCase):
    def setUp(self) -> None:
        self.token: Token = TokenFactory()
        self.user: User = self.token.user
        self.task: Task = TaskFactory(user=self.user)

    def test_add_tag(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        tag: TaskTag = TaskTagFactory(user=self.user)

        self.assertEqual(self.task.tags.count(), 0)

        response = self.client.patch(f'/tasks/{self.task.pk}', {
            'tags': [tag.pk, ]
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.task.tags.count(), 1)

    def test_add_non_existent_tag(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.assertEqual(self.task.tags.count(), 0)

        response = self.client.patch(f'/tasks/{self.task.pk}', {
            'tags': [2, ]
        })

        self.assertEqual(response.status_code, 400)
        self.assertTrue('object does not exist.' in response.json()['tags'][0])

    def test_add_tag_not_same_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        tag: TaskTag = TaskTagFactory()

        self.assertNotEqual(tag.user, self.user)

        response = self.client.patch(f'/tasks/{self.task.pk}', {
            'tags': [tag.pk, ]
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual('This tag is not owned by the user.', response.json()['tags'][0])


class TaskTagListTests(APITransactionTestCase):
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

    def test_add_tag(self):
        self.assertEqual(TaskTag.objects.filter(user=self.user).count(), 0)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.post('/tasks/tags/', {
            'name': 'new tag',
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'new tag')
        self.assertEqual(response.json()['task_set'],  [])
        self.assertEqual(TaskTag.objects.filter(user=self.user).count(), 1)

    def test_add_tag_same_name(self):
        tag: TaskTag = TaskTagFactory(user=self.user)

        self.assertEqual(TaskTag.objects.filter(user=self.user).count(), 1)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.post('/tasks/tags/', {
            'name': tag.name,
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(TaskTag.objects.filter(user=self.user).count(), 1)

    def test_add_tag_same_name_different_user(self):
        tag: TaskTag = TaskTagFactory(user=self.user)
        new_token: Token = TokenFactory()

        self.assertEqual(TaskTag.objects.filter(user=self.user).count(), 1)
        self.assertEqual(TaskTag.objects.filter(user=new_token.user).count(), 0)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)

        response = self.client.post('/tasks/tags/', {
            'name': tag.name,
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], tag.name)
        self.assertEqual(response.json()['task_set'], [])
        self.assertEqual(TaskTag.objects.filter(user=self.user).count(), 1)
        self.assertEqual(TaskTag.objects.filter(user=new_token.user).count(), 1)

    def test_add_tag_not_logged_in(self):
        response = self.client.post('/tasks/tags/', {
            'name': 'test',
        })

        self.assertEqual(response.status_code, 401)


class TaskTagDetailTests(APITestCase):
    def setUp(self) -> None:
        self.token: Token = TokenFactory()
        self.user: User = self.token.user
        self.tag: TaskTag = TaskTagFactory(user=self.user)

    def test_get_tag(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(f'/tasks/tags/{self.tag.pk}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.tag.pk)
        self.assertEqual(response.json()['name'], self.tag.name)
        self.assertEqual(response.json()['task_set'], [])

        task: Task = TaskFactory(user=self.user)
        task.tags.add(self.tag)
        task.save()

        response = self.client.get(f'/tasks/tags/{self.tag.pk}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['task_set'], [task.pk])

    def test_get_non_existent_tag(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(f'/tasks/tags/{self.tag.pk + 1}/')

        self.assertEqual(response.status_code, 404)

    def test_get_unauthorized_tag(self):
        new_token: Token = TokenFactory()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        response = self.client.get(f'/tasks/tags/{self.tag.pk}/')

        self.assertEqual(response.status_code, 403)

    def test_get_tag_not_logged_in(self):
        response = self.client.get(f'/tasks/tags/{self.tag.pk}/')

        self.assertEqual(response.status_code, 401)
