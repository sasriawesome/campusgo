from django.apps import AppConfig as AppConfigBase
from django.utils.translation import gettext_lazy as _


class AppConfig(AppConfigBase):
    name = 'campusgo.lectures'
    label = 'campusgo_lectures'
    verbose_name = _('CampusGo Lectures')
