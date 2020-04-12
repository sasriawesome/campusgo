# Generated by Django 2.2.10 on 2020-04-12 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campusgo_persons', '0004_auto_20200412_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='relation',
            field=models.PositiveIntegerField(choices=[(1, 'Father'), (2, 'Mother'), (5, 'Husband'), (6, 'Wife'), (4, 'Children'), (3, 'Sibling'), (99, 'Other')], default=99, verbose_name='relation'),
        ),
        migrations.AlterField(
            model_name='formaleducation',
            name='status',
            field=models.CharField(choices=[('FNS', 'Finished'), ('ONG', 'Ongoing'), ('UNF', 'Unfinished')], default='ONG', max_length=5, verbose_name='current status'),
        ),
        migrations.AlterField(
            model_name='nonformaleducation',
            name='status',
            field=models.CharField(choices=[('FNS', 'Finished'), ('ONG', 'Ongoing'), ('UNF', 'Unfinished')], default='ONG', max_length=5, verbose_name='current status'),
        ),
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='person',
            name='last_education_level',
            field=models.CharField(choices=[(0, 'SD'), (1, 'SMP'), (2, 'SMA'), (3, 'D1'), (4, 'D2'), (5, 'D3'), (6, 'D4'), (7, 'S1'), (8, 'S2'), (9, 'S3')], default=2, max_length=5, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='status',
            field=models.CharField(choices=[('ACT', 'Active'), ('INC', 'Inactive')], default='ACT', max_length=5, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='working',
            name='employment',
            field=models.CharField(choices=[('CTR', 'Contract'), ('FXD', 'Fixed'), ('OSR', 'Outsource'), ('ELS', 'Else')], default='CTR', max_length=5, verbose_name='employment'),
        ),
        migrations.AlterField(
            model_name='working',
            name='status',
            field=models.CharField(choices=[('FNS', 'Finished'), ('ONG', 'Ongoing'), ('UNF', 'Unfinished')], default='ONG', max_length=5, verbose_name='current status'),
        ),
    ]
