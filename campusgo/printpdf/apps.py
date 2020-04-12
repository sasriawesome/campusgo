from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'campusgo.printpdf'
    label = 'campusgo_printpdf'
    verbose_name = 'CampusGo PrintPDF'
