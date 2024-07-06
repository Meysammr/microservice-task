from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from .models import Task, Project
from .utils import send_notification



@shared_task
def send_task_reminders():
    due_date_threshold = now() + timedelta(days=1)
    tasks = Task.objects.filter(due_date__lte=due_date_threshold, status='pending')

    for task in tasks:
        send_mail(
            'Task Reminder',
            f'Reminder: The task "{task.title}" is due within 24 hours.',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )

@shared_task
def send_daily_project_summary():
    projects = Project.objects.all()

    summary = []
    for project in projects:
        summary.append(f'Project: {project.name}')
        tasks = project.tasks.all()
        for task in tasks:
            summary.append(f'  - Task: {task.title} (Status: {task.status})')

    send_mail(
        'Daily Project Summary',
        '\n'.join(summary),
        'from@example.com',
        ['to@example.com'],  # Replace with actual recipient email
        fail_silently=False,
    )

@shared_task
def send_daily_project_summary():
    projects = Project.objects.all()
    summary = []
    for project in projects:
        summary.append(f'Project: {project.name}')
        tasks = project.tasks.all()
        for task in tasks:
            summary.append(f'  - Task: {task.title} (Status: {task.status})')

    send_mail(
        'Daily Project Summary',
        '\n'.join(summary),
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )

    send_notification('Daily project summary report has been generated.')