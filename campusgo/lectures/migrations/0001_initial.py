# Generated by Django 2.2.10 on 2020-02-27 01:39

import campusgo.lectures.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('is_deleted', models.BooleanField(default=False, editable=False, verbose_name='is deleted?')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('code', models.CharField(max_length=128, verbose_name='Code')),
                ('date_start', models.DateField(default=django.utils.timezone.now, verbose_name='Date start')),
                ('default_time_start', models.TimeField(default=django.utils.timezone.now, verbose_name='Time start')),
                ('duration', models.PositiveIntegerField(help_text='Lecture duration in minutes', verbose_name='Duration')),
                ('series', models.PositiveIntegerField(help_text='Total Meet Up', verbose_name='Series')),
                ('status', models.CharField(choices=[('PND', 'Pending'), ('REG', 'Registration'), ('PRE', 'Preparation'), ('ONG', 'Ongoing'), ('END', 'End'), ('CMP', 'Complete')], default=campusgo.lectures.models.LectureStatus('PND'), max_length=3, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Lecture',
                'verbose_name_plural': 'Lectures',
            },
        ),
        migrations.CreateModel(
            name='LectureSchedule',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('is_deleted', models.BooleanField(default=False, editable=False, verbose_name='is deleted?')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('session', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(50)], verbose_name='Session')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Date')),
                ('time_start', models.TimeField(default=django.utils.timezone.now, verbose_name='Time start')),
                ('time_end', models.TimeField(default=django.utils.timezone.now, verbose_name='Time end')),
                ('type', models.CharField(choices=[('1', 'Meeting'), ('2', 'E-Learning'), ('99', 'Subtitution'), ('3', 'Mid Exam'), ('4', 'Final Exam')], default='1', max_length=3, verbose_name='Type')),
            ],
            options={
                'verbose_name': 'Lecture Schedule',
                'verbose_name_plural': 'Lecture Schedules',
            },
        ),
    ]