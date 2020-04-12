from django.utils import translation
from django.contrib import admin

from wagtail.admin.edit_handlers import (
    ObjectList, TabbedInterface, FieldPanel,
    MultiFieldPanel, InlinePanel, FieldRowPanel)
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from django_abstracts.academics.enums import ManagementLevel

from ...autocompletes.edit_handlers import AutocompletePanel
from ..models import Curriculum, ManagementUnit, SchoolYear, CourseGroup, CourseType, AcademicYear, Course
from .chooser import CourseChooser

_ = translation.gettext_lazy

LIST_PER_PAGE = 20


class ManagementUnitModelAdmin(ModelAdmin):
    search_fields = ['name', 'code']
    model = ManagementUnit
    menu_icon = 'fa-sitemap'
    menu_label = _('Management Unit')
    list_per_page = LIST_PER_PAGE
    list_display = ['unit_name', 'code', 'name', 'parent']
    list_filter = ['type']
    edit_handler = ObjectList([
        MultiFieldPanel([
            FieldPanel('parent'),
            FieldPanel('name'),
            FieldPanel('type'),
            FieldPanel('code'),
        ])
    ])

    def unit_name(self, obj):
        return "{} {}".format('---' * obj.level, obj.name)


class ProgramStudyFilter(admin.SimpleListFilter):
    title = 'Program Study'
    parameter_name = 'rmu__code'

    def lookups(self, request, model_admin):
        rmu = ManagementUnit.objects.filter(type=ManagementLevel.PROGRAM_STUDY.value)
        return [(unit.code, unit.name) for unit in rmu]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(rmu__code=self.value())
        return queryset


class SchoolYearModelAdmin(ModelAdmin):
    menu_icon = 'fa-calendar'
    menu_label = _('School Year')
    list_per_page = LIST_PER_PAGE
    model = SchoolYear
    edit_handler = ObjectList([
        MultiFieldPanel([
            FieldPanel('year_start'),
            FieldPanel('year_end'),
        ])
    ])


class AcademicYearModelAdmin(ModelAdmin):
    menu_icon = 'fa-calendar'
    list_per_page = LIST_PER_PAGE
    model = AcademicYear
    inspect_view_enabled = True
    list_display = ['school_year', 'semester', 'date_start', 'date_end']

    academic_year_panels = [
        MultiFieldPanel([
            AutocompletePanel('school_year'),
            FieldPanel('semester'),
            FieldPanel('date_start'),
            FieldPanel('date_end'),
        ])
    ]

    # TODO Next Feature Sprint 2
    activities_panels = [
        InlinePanel(
            'semester_activities',
            panels=[
                AutocompletePanel('rmu'),
                AutocompletePanel('school_year'),
                FieldPanel('activity'),
                FieldPanel('date_start'),
                FieldPanel('date_end'),
            ])
    ]

    edit_handler = ObjectList(academic_year_panels, heading=_('Academic Year'))


class CourseGroupModelAdmin(ModelAdmin):
    model = CourseGroup
    menu_icon = 'fa-book'
    menu_label = _('Course Group')
    list_display = ('code', 'alias', 'name')


class CourseTypeModelAdmin(ModelAdmin):
    model = CourseType
    menu_icon = 'fa-book'
    menu_label = _('Course Type')
    list_display = ('code', 'alias', 'name')


class CourseModelAdmin(ModelAdmin):
    model = Course
    list_per_page = LIST_PER_PAGE
    search_fields = ['name', 'inner_id']
    menu_icon = 'fa-book'
    inspect_view_enabled = True
    list_filter = ['rmu', 'is_active']
    list_display = ['inner_id', 'name', 'rmu', 'group', 'level', 'oyear']

    def oyear(self, obj):
        return obj.year_offered

    def rmu_code(self, obj):
        return obj.rmu.code

    def group(self, obj):
        return obj.course_group.alias

    course_panels = [
        MultiFieldPanel([
            FieldPanel('rmu'),
            FieldPanel('old_code'),
            FieldPanel('name'),
            FieldPanel('description'),
        ], heading=_('description')),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('course_type'),
                FieldPanel('course_group'),
            ], classname="label-above"),
            FieldRowPanel([
                FieldPanel('level'),
                FieldPanel('year_offered'),
            ], classname="label-above")
        ], heading=_('course group'))
    ]

    prerequisite_panels = [
        InlinePanel(
            'requisites', panels=[
                MultiFieldPanel([
                    FieldPanel('requisite', widget=CourseChooser),
                    FieldPanel('score'),
                ])
            ])
    ]

    option_panels = [
        MultiFieldPanel([
            FieldPanel('has_lpu'),
            FieldPanel('has_dictate'),
            FieldPanel('has_teaching_material'),
            FieldPanel('has_practice_program'),
            FieldPanel('is_active'),
        ])
    ]

    edit_handler = TabbedInterface([
        ObjectList(course_panels, heading=_('Course')),
        ObjectList(prerequisite_panels, heading=_('Prerequesites')),
        ObjectList(option_panels, heading=_('Options')),
    ])


class CurriculumModelAdmin(ModelAdmin):
    model = Curriculum
    list_per_page = LIST_PER_PAGE
    search_fields = ['name', 'code']
    menu_icon = 'fa-book'
    inspect_view_enabled = True
    list_display = ['name', 'code', 'rmu', 'sks_graduate', 'is_active']
    list_filter = [ProgramStudyFilter, 'is_active']

    course_panels = [
        InlinePanel(
            'curriculum_courses',
            panels=[
                FieldPanel('course', widget=CourseChooser),
                FieldRowPanel([
                    FieldPanel('semester_number'),
                    FieldPanel('semester_type'),
                ]),
                FieldRowPanel([
                    FieldPanel('sks_meeting'),
                    FieldPanel('sks_practice'),
                ]),
                FieldRowPanel([
                    FieldPanel('sks_field_practice'),
                    FieldPanel('sks_simulation'),
                ])
            ])
    ]

    curriculum_panels = [
        MultiFieldPanel([
            FieldPanel('rmu'),
            FieldPanel('year'),
            FieldPanel('sks_graduate'),
            FieldPanel('is_active'),
        ])
    ]

    edit_handler = TabbedInterface([
        ObjectList(curriculum_panels, heading=_('Curriculum')),
        ObjectList(course_panels, heading=_('Courses'))
    ])

    def inspect_view(self, request, instance_pk):
        ins = self.model.objects.get(pk=instance_pk)
        ins.get_courses_by_semester()
        return super().inspect_view(request, instance_pk)


class AcademicModelAdminGroup(ModelAdminGroup):
    menu_label = _('Academic')
    menu_icon = 'fa-mortar-board'
    items = [
        ManagementUnitModelAdmin,
        AcademicYearModelAdmin,
        SchoolYearModelAdmin
    ]


class CourseModelAdminGroup(ModelAdminGroup):
    menu_label = _('Courses')
    menu_icon = 'fa-book'
    items = [
        CurriculumModelAdmin,
        CourseModelAdmin,
        CourseGroupModelAdmin,
        CourseTypeModelAdmin,
    ]


modeladmin_register(AcademicModelAdminGroup)
modeladmin_register(CourseModelAdminGroup)
