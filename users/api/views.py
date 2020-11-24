from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from tasks.models import Task
from tasks.api.serializers import TaskExportSerializer
from users.models import User
from users.api.serializers import UserSerializer, UserCreationSerializer


@api_view(['POST'])
def users_list(request):
    if request.method == 'POST':
        serializer = UserCreationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserPermission(BasePermission):
    message = 'Access denied'

    def has_object_permission(self, request, view, obj):
        return request.user.pk == obj.pk


class UserDetail(APIView):
    permission_classes = [IsAuthenticated, UserPermission]

    def get(self, request):
        user: User = User.objects.get(pk=self.request.user.pk)
        serializer = UserSerializer(user)

        return Response(serializer.data, status=HTTP_200_OK)


class DownloadUserData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=self.request.user)
        serializer = TaskExportSerializer(tasks, many=True)

        return Response(serializer.data, status=HTTP_200_OK)
