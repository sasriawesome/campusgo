from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'campusgo.core'
    label = 'campusgo_core'
    verbose_name = 'CampusGo Core'
