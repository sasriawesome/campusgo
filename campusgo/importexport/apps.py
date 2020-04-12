from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'campusgo.importexport'
    label = 'campusgo_importexport'
    verbose_name = 'CampusGo ImportExport'
