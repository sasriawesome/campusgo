from django.utils import translation
from wagtail.core.models import Page

_ = translation.gettext_lazy


class HomePage(Page):
    class Meta:
        verbose_name = _('Home Page')
        verbose_name_plural = _('Home Pages')

    template = 'campusgo_pages/homepage.html'