from django.utils import translation, html

from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.admin.edit_handlers import (
    ObjectList, TabbedInterface, FieldPanel,
    MultiFieldPanel, InlinePanel)
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from ..models import Syllabus
from .chooser import (
    CourseChooser
)

_ = translation.gettext_lazy

LIST_PER_PAGE = 20



# TODO Next Feature Sprint 2
class SyllabusModelAdmin(ModelAdmin):
    list_per_page = LIST_PER_PAGE
    model = Syllabus
    inspect_view_enabled = True
    style = '<span style="font-size;font-size: .8em; color: yellow;">'
    menu_label = html.format_html(_('E-Syllabus <br/>{}(Feature Sprint 2)</span>').format(style))
    menu_icon = 'fa-book'
    search_fields = ['title', 'course']
    list_display = ['inner_id', 'title', 'course', 'creator']

    edit_handler = TabbedInterface([
        ObjectList([
            MultiFieldPanel([
                FieldPanel('title'),
                FieldPanel('course', widget=CourseChooser),
                FieldPanel('description'),
            ], heading=_('Descriptions')),
            StreamFieldPanel('body')
        ], heading=_('Syllabus')),
        ObjectList([
            InlinePanel('lecture_programs', panels=[
                StreamFieldPanel('programs')
            ], max_num=1)
        ], heading=_('Programs'))
    ])


class SyllabusAdminGroup(ModelAdminGroup):
    menu_label = _('Courses')
    menu_icon = 'fa-book'
    items = [
        SyllabusModelAdmin,
    ]


modeladmin_register(SyllabusAdminGroup)
