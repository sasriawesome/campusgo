from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'campusgo.persons'
    label = 'campusgo_persons'
    verbose_name = 'CampusGo Persons'
