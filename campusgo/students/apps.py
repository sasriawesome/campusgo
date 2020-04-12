from django.apps import AppConfig as AppConfigBase

class AppConfig(AppConfigBase):
    name = 'campusgo.students'
    label = 'campusgo_students'
    verbose_name = 'CampusGo Students'
