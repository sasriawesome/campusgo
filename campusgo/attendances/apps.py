from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'campusgo.attendances'
    label = 'campusgo_attendances'
    verbose_name = 'CampusGo Attendances'
