from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, InlinePanel,
    TabbedInterface, ObjectList)
from wagtail.contrib.modeladmin.options import modeladmin_register, ModelAdminGroup

from campusgo.admin.admin import ModelAdmin
from campusgo.autocompletes.edit_handlers import AutocompletePanel
from campusgo.enrollments.models import Enrollment


class EnrollmentModelAdmin(ModelAdmin):
    menu_label = _('Enrollments')
    menu_icon = 'fa-wpforms'
    model = Enrollment
    list_per_page = 20

    edit_handler = TabbedInterface([
        ObjectList([
            MultiFieldPanel([
                AutocompletePanel('student'),
                FieldPanel('academic_year'),
                FieldPanel('note'),
                FieldPanel('coach_review'),
                FieldPanel('status'),
            ])
        ], heading=_('Form')),
        ObjectList([
            InlinePanel( 'lectures', panels=[
                AutocompletePanel('lecture'),
                FieldPanel('criteria'),
            ])
        ], heading=_('Lectures'))
    ])


class EnrollmentModelAdminGroup(ModelAdminGroup):
    menu_icon = 'fa-wpforms'
    menu_label = _('Enrollments')
    items = [
        EnrollmentModelAdmin
    ]

modeladmin_register(EnrollmentModelAdminGroup)