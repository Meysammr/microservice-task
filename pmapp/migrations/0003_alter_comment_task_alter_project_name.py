# Generated by Django 4.2.10 on 2024-07-03 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pmapp', '0002_alter_comment_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='pmapp.task'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=225, unique=True),
        ),
    ]
