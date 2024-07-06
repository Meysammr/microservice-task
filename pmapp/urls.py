from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('projects/<int:id>/', views.ProjectRetrieveUpdateDeleteView.as_view(), name='project-retrieve-update-destroy'),
    path('tasks/', views.TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:id>/', views.TaskRetrieveUpdateDeleteView.as_view(), name='task-retrieve-update-destroy'),
    path('tasks/<int:id>/comments/', views.CommentListCreateAPIView.as_view(), name='comment-list-create'),
]
