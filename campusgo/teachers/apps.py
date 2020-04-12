from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'campusgo.teachers'
    label = 'campusgo_teachers'
    verbose_name = 'CampusGo Teachers'
