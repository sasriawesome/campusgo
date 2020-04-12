from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, ObjectList, InlinePanel, MultiFieldPanel
from wagtail.contrib.modeladmin.options import modeladmin_register, ModelAdminGroup

from campusgo.admin.admin import ModelAdmin
from campusgo.registrations.models import Program, Price, Registration


class ProgramModelAdmin(ModelAdmin):
    model = Program

    edit_handler = ObjectList([
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('description'),
            FieldPanel('program_study'),
            FieldPanel('is_active'),
        ], heading=_('Program')),
        InlinePanel('prices', panels=[
            FieldPanel('name'),
            FieldPanel('note'),
            FieldPanel('price'),
        ], heading=_('Prices'))
    ])


class RegistrationModelAdminGroup(ModelAdminGroup):
    menu_label = 'Registration'
    items = [
        ProgramModelAdmin
    ]


modeladmin_register(RegistrationModelAdminGroup)
