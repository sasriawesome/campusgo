from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdminGroup
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.shortcuts import redirect, reverse

from wagtail.admin.edit_handlers import ObjectList, TabbedInterface, FieldPanel, MultiFieldPanel
from wagtail.contrib.modeladmin.options import modeladmin_register
from campusgo.admin.admin import ModelAdmin
from campusgo.autocompletes.edit_handlers import AutocompletePanel
from campusgo.teachers.models import Teacher, TeacherPersonal
from campusgo.academic.admin import ProgramStudyFilter
from campusgo.persons.admin import PersonModelAdmin


class TeacherPersonalModelAdmin(PersonModelAdmin):
    model = TeacherPersonal
    menu_icon = 'fa-user'
    menu_label = _('Teacher Personal')


class TeacherModelAdmin(ModelAdmin):
    model = Teacher
    menu_icon = 'fa-user'
    inspect_view_enabled = True
    list_filter = ['is_active', ProgramStudyFilter]
    search_fields = ['tid', 'person__fullname', 'rmu__name']
    list_display = ['tid', 'name', 'rmu', 'is_active']
    edit_handler = ObjectList([
        MultiFieldPanel([
            FieldPanel('tid'),
            AutocompletePanel('person'),
            AutocompletePanel('rmu'),
            AutocompletePanel('courses'),
            FieldPanel('is_active')
        ])
    ], heading=_('Teacher'))


class TeacherModelAdminGroup(ModelAdminGroup):
    menu_order = 103
    menu_label = _('Teachers')
    menu_icon = 'fa-user-circle'
    items = [
        TeacherModelAdmin,
        TeacherPersonalModelAdmin,
    ]

    def get_submenu_items(self):
        sub_menuitems = super().get_submenu_items()
        return sub_menuitems


modeladmin_register(TeacherModelAdminGroup)
