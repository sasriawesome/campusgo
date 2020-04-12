from django.apps import AppConfig as AppConfigBase

class AppConfig(AppConfigBase):
    name = 'campusgo.users'
    label = 'campusgo_users'
    verbose_name = 'CampusGo Users'