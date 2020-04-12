from django.apps import AppConfig as AppConfigBase
from django.utils.translation import gettext_lazy as _


class AppConfig(AppConfigBase):
    name = 'campusgo.academic'
    label = 'campusgo_academic'
    verbose_name = _("CampusGo Academic")
