# Generated by Django 2.2.10 on 2020-02-26 23:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('wagtailimages', '0001_squashed_0021'),
        ('auth', '0011_update_proxy_permissions'),
        ('campusgo_core', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CampusGoSettings',
            new_name='CampusGoSetting',
        ),
    ]
