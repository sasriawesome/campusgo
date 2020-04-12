from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from ..models import (
    CourseRequisite, AcademicYear, SchoolYear, CourseGroup, CourseType,
    ManagementUnit, Curriculum, Course, CourseEqualizer,
    CurriculumCourse)


@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ['code', 'year_start', 'year_end']


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['code', 'school_year', 'semester', 'date_start', 'date_end']


@admin.register(ManagementUnit)
class ManagementUnitAdmin(MPTTModelAdmin):
    list_filter = ['level']
    list_display = ['name', 'code', 'parent', 'courses', 'students', 'teachers']

    def courses(self, obj):
        return obj.total_cum_courses

    def students(self, obj):
        return obj.total_cum_students

    def teachers(self, obj):
        return obj.total_cum_teachers

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return ManagementUnit.objects.get_with_summary(qs)


class CurriculumCourseInline(admin.TabularInline):
    extra = 0
    model = CurriculumCourse
    raw_id_fields = ['course']


class ProgramStudyFilter(admin.SimpleListFilter):
    title = 'Program Study'
    parameter_name = 'rmu__code'

    def lookups(self, request, model_admin):
        return [(rmu.code, rmu.name) for rmu in ManagementUnit.objects.filter(status='4')]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(rmu__code=self.value())
        return queryset


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    search_fields = ['name', 'rmu__name']
    inlines = [CurriculumCourseInline]
    list_filter = [ProgramStudyFilter]
    list_display = [
        'name', 'rmu',
        'sks_graduate',
        'mandatory',
        'choice',
        'interest',
        'research',
        'meeting',
        'practice',
        'field_practice',
        'simulation'
    ]
    raw_id_fields = ['rmu']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return Curriculum.objects.get_with_summary(qs)

    def mandatory(self, obj):
        return obj.sks_mandatory

    def choice(self, obj):
        return obj.sks_choice

    def interest(self, obj):
        return obj.sks_interest

    def research(self, obj):
        return obj.sks_research

    def meeting(self, obj):
        return obj.sks_meeting

    def practice(self, obj):
        return obj.sks_practice

    def field_practice(self, obj):
        return obj.sks_field_practice

    def simulation(self, obj):
        return obj.sks_simulation


@admin.register(CurriculumCourse)
class CurriculumCourseAdmin(admin.ModelAdmin):
    search_fields = ['course__name', 'curriculum__year']
    list_filter = ['curriculum']
    list_select_related = ['course']
    list_display = [
        'course_name', 'curriculum', 'semester_number',
        'sks_meeting', 'sks_practice', 'sks_field_practice',
        'sks_simulation', 'sks_total']
    raw_id_fields = ['course', 'curriculum']

    def course_name(self, obj):
        return obj.course_name


@admin.register(CourseType)
class CourseType(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'code', 'alias']


@admin.register(CourseGroup)
class CourseGroup(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'code', 'alias']


class CoursePreRequisiteInline(admin.TabularInline):
    extra = 0
    fk_name = 'course'
    model = CourseRequisite


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [CoursePreRequisiteInline]
    list_display = ['inner_id', 'name', 'rmu', 'level',
                    'course_type', 'course_group', 'is_active']
    list_filter = ['rmu', 'year_offered']


@admin.register(CourseEqualizer)
class CourseEqualizerAdmin(admin.ModelAdmin):
    search_fields = ['old_course__course__name']
    list_display = ['old_course', 'new_course', 'sks_new_course', 'sks_old_course']
