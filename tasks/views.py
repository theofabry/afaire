from django.db import IntegrityError
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from tasks.models import Task, TaskTag
from tasks.serializers import TaskSerializer, TaskTagSerializer


class TaskPermission(BasePermission):
    message = 'Access denied'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class TaskTagPermission(BasePermission):
    message = 'Access denied'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class TaskList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks_by_date = Task.objects.get_tasks_by_date(user=self.request.user)

        return Response(tasks_by_date)

    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={'request': self.request})

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    permission_classes = [IsAuthenticated, TaskPermission]

    def get_object(self, task_pk):
        try:
            task: Task = Task.objects.get(pk=task_pk)
            self.check_object_permissions(self.request, task)

            return Task.objects.get(pk=task_pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, task_pk):
        task: Task = self.get_object(task_pk=task_pk)
        serializer = TaskSerializer(task)

        return Response(serializer.data)

    def patch(self, request, task_pk):
        task: Task = self.get_object(task_pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, task_pk):
        task: Task = self.get_object(task_pk)
        task.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class TaskTagList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tags = TaskTag.objects.filter(user=self.request.user)
        serializer = TaskTagSerializer(tags, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = TaskTagSerializer(data=self.request.data, context={'request': self.request})

        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError:
                return Response({'name': ['This name already exists.']}, status=HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class TaskTagDetail(APIView):
    permission_classes = [IsAuthenticated, TaskTagPermission]

    def get_object(self, task_tag_pk):
        try:
            task_tag: TaskTag = TaskTag.objects.get(pk=task_tag_pk)
            self.check_object_permissions(self.request, task_tag)

            return TaskTag.objects.get(pk=task_tag_pk)
        except TaskTag.DoesNotExist:
            raise Http404

    def get(self, request, task_tag_pk):
        task_tag: Task = self.get_object(task_tag_pk=task_tag_pk)
        serializer = TaskTagSerializer(task_tag)

        return Response(serializer.data)
