# Generated by Django 2.2.10 on 2020-02-27 05:19

import campusgo.enrollments.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import modelcluster.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('campusgo_lectures', '0003_auto_20200227_0839'),
        ('campusgo_academic', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campusgo_students', '0002_auto_20200227_0839'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('is_deleted', models.BooleanField(default=False, editable=False, verbose_name='is deleted?')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Register number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('note', models.TextField(blank=True, max_length=256, null=True, verbose_name='Note for coach')),
                ('coach_review', models.TextField(blank=True, max_length=256, null=True, verbose_name='Coach review')),
                ('status', models.CharField(choices=[('TRASH', 'TRASH'), ('DRAFT', 'DRAFT'), ('SUBMITTED', 'SUBMITTED'), ('REVISION', 'REVISION'), ('VALID', 'VALID')], default=campusgo.enrollments.models.EnrollmentStatus('DRAFT'), max_length=2, verbose_name='Status')),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campusgo_academic.AcademicYear', verbose_name='Academic Year')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='enrollment_creator', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('deleted_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='enrollment_deleter', to=settings.AUTH_USER_MODEL, verbose_name='deleter')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campusgo_students.Student', verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Enrollment',
                'verbose_name_plural': 'Enrollments',
            },
        ),
        migrations.CreateModel(
            name='EnrollmentPlan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('is_deleted', models.BooleanField(default=False, editable=False, verbose_name='is deleted?')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('criteria', models.CharField(choices=[('1', 'NEW'), ('2', 'REMEDY')], default='1', max_length=2, verbose_name='Criteria')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='enrollmentplan_creator', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('deleted_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='enrollmentplan_deleter', to=settings.AUTH_USER_MODEL, verbose_name='deleter')),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campusgo_lectures.Lecture', verbose_name='Lecture')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campusgo_students.Student', verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Enrollment Plan',
                'verbose_name_plural': 'Enrollment Plans',
                'unique_together': {('student', 'lecture')},
            },
        ),
        migrations.CreateModel(
            name='EnrollmentItem',
            fields=[
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('is_deleted', models.BooleanField(default=False, editable=False, verbose_name='is deleted?')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('criteria', models.CharField(choices=[('1', 'NEW'), ('2', 'REMEDY')], default=campusgo.enrollments.models.EnrollmentCriteria('1'), max_length=2, verbose_name='Criteria')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='enrollmentitem_creator', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('deleted_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='enrollmentitem_deleter', to=settings.AUTH_USER_MODEL, verbose_name='deleter')),
                ('enrollment', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='lectures', to='campusgo_enrollments.Enrollment', verbose_name='Enrolment')),
                ('lecture', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='campusgo_lectures.Lecture', verbose_name='Lecture')),
            ],
            options={
                'verbose_name': 'Enrollment Item',
                'verbose_name_plural': 'Enrollment Items',
                'unique_together': {('enrollment', 'lecture')},
            },
        ),
    ]