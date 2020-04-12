from django.apps import AppConfig as  AppConfigBase


class AppConfig(AppConfigBase):
    name = 'campusgo.admin'
    label = 'campusgo_admin'
    verbose_name = 'CampusGo Admin'
