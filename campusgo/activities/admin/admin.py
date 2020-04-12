from django.utils import translation, html
from wagtail.admin.edit_handlers import ObjectList, FieldPanel, MultiFieldPanel
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from ...autocompletes.edit_handlers import AutocompletePanel
from ..models import AcademicActivity

_ = translation.gettext_lazy

LIST_PER_PAGE = 20


# TODO Next Feature Sprint 2
class AcademicActivityModelAdmin(ModelAdmin):
    list_per_page = LIST_PER_PAGE
    model = AcademicActivity
    menu_icon = 'fa-calendar-check-o'
    style = '<span style="font-size;font-size: .8em; color: yellow;">'
    menu_label = html.format_html(_('Activities <br/>{}(Feature Sprint 2)</span>').format(style))
    search_field = ['activity', 'rmu__name']
    list_filter = ['date_start', 'date_end', 'school_year', 'rmu']
    list_display = ['date_start', 'date_end', 'school_year', 'description']

    edit_handler = ObjectList([
        MultiFieldPanel([
            FieldPanel('rmu'),
            AutocompletePanel('academic_year'),
            FieldPanel('activity'),
            FieldPanel('date_start'),
            FieldPanel('date_end'),
        ])
    ])

    def description(self, obj):
        return html.format_html(obj.activity)


class AcademicModelAdminGroup(ModelAdminGroup):
    menu_label = _('Academic')
    menu_icon = 'fa-mortar-board'
    items = [
        AcademicActivityModelAdmin,
    ]


modeladmin_register(AcademicModelAdminGroup)
