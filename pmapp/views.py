from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.cache import cache

from .utils import cache_get_or_set, cache_invalidate
from .models import Project, Task, Comment
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer


class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        key = 'project_list'
        projects = cache_get_or_set(key, lambda: super().list(request, *args, **kwargs).data)
        return Response(projects)


class ProjectRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'


class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        key = 'task_list'
        tasks = cache_get_or_set(key, lambda: super().list(request, *args, **kwargs).data)
        return Response(tasks)


class TaskRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'


class CommentListCreateAPIView(APIView):

    def post(self, request, id):
        task = Task.objects.get(id=id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        comments = Comment.objects.filter(task_id=id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
