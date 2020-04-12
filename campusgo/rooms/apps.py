from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'campusgo.rooms'
    label = 'campusgo_rooms'
    verbose_name = 'CampusGo Rooms'
