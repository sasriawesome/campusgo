from django.apps import AppConfig as AppConfigBase
from django.utils.translation import gettext_lazy as _


class AppConfig(AppConfigBase):
    name = 'campusgo.enrollments'
    label = 'campusgo_enrollments'
    verbose_name = _('CampusGo Enrollments')
