# Generated by Django 2.2.10 on 2020-02-28 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campusgo_registrations', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='price',
            old_name='title',
            new_name='name',
        ),
        migrations.AddField(
            model_name='price',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Price'),
        ),
    ]