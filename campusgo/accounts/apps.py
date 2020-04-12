from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'campusgo.accounts'
    label = 'campusgo_accounts'
    verbose_name = 'CampusGo Accounts'
