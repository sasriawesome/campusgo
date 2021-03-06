# Generated by Django 2.2.10 on 2020-02-27 01:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('campusgo_persons', '0002_personsettings'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campusgo_academic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('is_deleted', models.BooleanField(default=False, editable=False, verbose_name='is deleted?')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Register number')),
                ('sid', models.CharField(editable=False, max_length=128, unique=True, verbose_name='Student ID')),
                ('registration_id', models.CharField(max_length=128, verbose_name='Registration ID')),
                ('registration', models.CharField(choices=[('1', 'Reguler'), ('P', 'Transfer')], default='1', max_length=2, verbose_name='Registration')),
                ('status', models.CharField(choices=[('ACT', 'Active'), ('ALM', 'Alumni'), ('DRO', 'Drop out'), ('MVD', 'Moved'), ('MSC', 'Misc')], default='ACT', max_length=128, verbose_name='Status')),
                ('status_note', models.CharField(blank=True, max_length=256, null=True, verbose_name='Status note')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
                'permissions': (('register_student', 'Can Register New Student'),),
            },
        ),
        migrations.CreateModel(
            name='StudentScore',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('is_deleted', models.BooleanField(default=False, editable=False, verbose_name='is deleted?')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('numeric', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Numeric Score')),
                ('alphabetic', models.CharField(max_length=1, verbose_name='Alphabetic Score')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='student_scores', to='campusgo_academic.CurriculumCourse', verbose_name='Course')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='studentscore_creator', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('deleted_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='studentscore_deleter', to=settings.AUTH_USER_MODEL, verbose_name='deleter')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_campusgo_students.studentscore_set+', to='contenttypes.ContentType')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='campusgo_students.Student', verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Student Score',
                'verbose_name_plural': 'Student Scores',
            },
        ),
        migrations.CreateModel(
            name='StudentPersonal',
            fields=[
            ],
            options={
                'verbose_name': 'Student Personal',
                'verbose_name_plural': 'Student Personals',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('campusgo_persons.person',),
        ),
        migrations.CreateModel(
            name='ConversionScore',
            fields=[
                ('studentscore_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='campusgo_students.StudentScore')),
                ('ori_code', models.CharField(max_length=128, verbose_name='Origin Code')),
                ('ori_name', models.CharField(max_length=128, verbose_name='Origin Name')),
                ('ori_numeric_score', models.DecimalField(decimal_places=2, default=1, max_digits=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='Origin Numeric')),
                ('ori_alphabetic_score', models.CharField(max_length=128, verbose_name='Origin Alphabetic')),
            ],
            options={
                'verbose_name': 'Conversion Score',
                'verbose_name_plural': 'Conversion Scores',
            },
            bases=('campusgo_students.studentscore',),
        ),
    ]
