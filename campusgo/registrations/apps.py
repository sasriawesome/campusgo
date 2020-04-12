from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'campusgo.registrations'
    label = 'campusgo_registrations'
    verbose_name = 'CampusGo Registrations'
