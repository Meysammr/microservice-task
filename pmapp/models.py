from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .utils import send_notification


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=225, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]

    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=225)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.task}'


@receiver(post_save, sender=Task)
def task_saved(sender, instance, created, **kwargs):
    if created:
        send_notification(f'A new task "{instance.title}" was created.')
    else:
        send_notification(f'The task "{instance.title}" was updated.')


@receiver(post_delete, sender=Task)
def task_deleted(sender, instance, **kwargs):
    send_notification(f'The task "{instance.title}" was deleted.')


@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs):
    if created:
        send_notification(f'New comment on task "{instance.task.title}": {instance.content}')
