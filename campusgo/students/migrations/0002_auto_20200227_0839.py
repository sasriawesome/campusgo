# Generated by Django 2.2.10 on 2020-02-27 01:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('campusgo_persons', '0002_personsettings'),
        ('campusgo_students', '0001_initial'),
        ('campusgo_academic', '0001_initial'),
        ('campusgo_teachers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='coach',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='campusgo_teachers.Teacher', verbose_name='Coach'),
        ),
        migrations.AddField(
            model_name='student',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_creator', to=settings.AUTH_USER_MODEL, verbose_name='creator'),
        ),
        migrations.AddField(
            model_name='student',
            name='deleted_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_deleter', to=settings.AUTH_USER_MODEL, verbose_name='deleter'),
        ),
        migrations.AddField(
            model_name='student',
            name='person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='campusgo_persons.Person', verbose_name='Person'),
        ),
        migrations.AddField(
            model_name='student',
            name='rmu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='campusgo_academic.ProgramStudy', verbose_name='Program Study'),
        ),
        migrations.AddField(
            model_name='student',
            name='year_of_force',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='campusgo_academic.SchoolYear', verbose_name='Year of force'),
        ),
    ]
