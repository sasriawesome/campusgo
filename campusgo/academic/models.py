from django.db import models
from django.utils import translation

from mptt.models import TreeForeignKey

from wagtail.search import index
from wagtail.core.models import Orderable
from modelcluster.models import ClusterableModel, ParentalKey

from django_numerators.models import NumeratorReset
from django_abstracts.academics.enums import ManagementLevel
from django_abstracts.academics.models import (
    ManagementUnitAbstract,
    SchoolYearAbstract,
    AcademicYearAbstract,
    CourseTypeAbstract,
    CourseGroupAbstract,
    CourseAbstract,
    CoursePreRequisiteAbstract,
    CurriculumAbstract,
    CurriculumCourseAbstract,
    CourseEqualizerAbstract,
)

from .managers import ManagementUnitManager, CurriculumManager, CurricullumCourseManager

_ = translation.gettext_lazy


class ManagementUnit(ManagementUnitAbstract):
    class Meta:
        verbose_name = _("management unit")
        verbose_name_plural = _("management units")

    objects = ManagementUnitManager()

    search_fields = [
        index.SearchField('name', partial_match=True),
        index.SearchField('code', partial_match=True),
    ]

    # Wagtail Autocomplete
    autocomplete_search_field = 'name'

    def autocomplete_label(self):
        # Wagtail Autocomplete Label
        return "{}".format(self.name)

    def __str__(self):
        return self.name


class SchoolYear(ClusterableModel, SchoolYearAbstract):
    class Meta:
        verbose_name = _("school year")
        verbose_name_plural = _("school years")

    # Wagtail Autocomplete
    autocomplete_search_field = 'code'

    def autocomplete_label(self):
        # Wagtail Autocomplete Label
        return "{}".format(self.code)

    def create_code(self):
        return "{}/{}".format(self.year_start, self.year_end)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = self.create_code()
        super().save(*args, **kwargs)


class AcademicYear(ClusterableModel, AcademicYearAbstract):
    class Meta:
        verbose_name = _("academic year")
        verbose_name_plural = _("academic years")

    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.PROTECT,
        verbose_name=_("school year")
    )

    # Wagtail Autocomplete
    autocomplete_search_field = 'code'

    def autocomplete_label(self):
        # Wagtail Autocomplete Label
        return "{}".format(self.code)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = "{} S{}".format(self.school_year, self.semester)
        super().save(*args, **kwargs)


class CourseType(CourseTypeAbstract):
    class Meta:
        verbose_name = _("course yype")
        verbose_name_plural = _("course types")
        ordering = ('code',)

    def __str__(self):
        return "{}".format(self.name)


class CourseGroup(CourseGroupAbstract):
    class Meta:
        verbose_name = _("Course Group")
        verbose_name_plural = _("Course Groups")
        ordering = ('code',)

    def __str__(self):
        return "{}".format(self.name)


class CourseManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).select_related(
            'rmu', 'course_type', 'course_group'
        )


class Course(index.Indexed, ClusterableModel, CourseAbstract):
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ('inner_id',)

    reset_mode = NumeratorReset.FIXED

    course_type = models.ForeignKey(
        CourseType,
        related_name='courses',
        on_delete=models.PROTECT,
        verbose_name=_("course type"))
    course_group = models.ForeignKey(
        CourseGroup,
        related_name='courses',
        on_delete=models.PROTECT,
        verbose_name=_("course group"))
    rmu = TreeForeignKey(
        ManagementUnit,
        on_delete=models.PROTECT,
        related_name='courses',
        verbose_name=_("management unit"))

    search_fields = [
        index.SearchField('name', partial_match=True),
        index.SearchField('inner_id', partial_match=True),
        index.FilterField('rmu'),
    ]

    # wagtail autocomplete
    autocomplete_search_field = 'name'

    def autocomplete_label(self):
        return "{} | {}".format(self.inner_id, self.name)

    def __str__(self):
        return "{}, {}".format(self.inner_id, self.name)

    def get_requisite(self):
        prerequesite = getattr(self, 'requisites', None)
        return [] if not prerequesite else prerequesite.all()

    @property
    def prerequisite(self):
        req = ", ".join([str(i.requisite.name) for i in self.get_requisite()])
        return req

    def get_doc_prefix(self):
        form = [self.rmu.code, self.course_type.code, self.course_group.code]
        doc_prefix = '{}{}{}'.format(*form)
        return doc_prefix

    def format_inner_id(self):
        """ Inner ID final format """
        form = [
            self.get_doc_prefix(),
            self.level,
            self.year_offered,
            self.format_number()
        ]
        self.inner_id = '{}{}{}{}'.format(*form)
        return self.inner_id

    def get_teachers(self):
        teachers = getattr(self, 'teachers', None)
        return [] if not teachers else teachers.all()

    def save(self, **kwargs):
        super().save(**kwargs)


class CourseRequisite(Orderable, CoursePreRequisiteAbstract):
    class Meta:
        verbose_name = _("Course prerequisite")
        verbose_name_plural = _("Course prerequisite")

    course = ParentalKey(
        Course,
        related_name="requisites",
        on_delete=models.CASCADE,
        verbose_name=_("course"))
    requisite = models.ForeignKey(
        Course, null=True, blank=True,
        related_name="prerequisites",
        on_delete=models.CASCADE,
        verbose_name=_("requisite"))

    def __str__(self):
        return ", ".join([str(self.course.name), str(self.requisite.name)])


class Curriculum(ClusterableModel, CurriculumAbstract):
    class Meta:
        verbose_name = _("Curriculum")
        verbose_name_plural = _("Curriculums")

    objects = CurriculumManager()

    rmu = TreeForeignKey(
        ManagementUnit,
        on_delete=models.PROTECT,
        related_name='curriculums',
        verbose_name=_("Program Study"),
        help_text=_("Management Unit"),
        limit_choices_to={
            'type': ManagementLevel.PROGRAM_STUDY.value
        },
    )

    def __str__(self):
        return self.name

    def create_code(self):
        self.code = "".join([self.rmu.code, self.year])

    def create_name(self):
        self.name = "{} {}".format(self.rmu.name, self.year)

    def save(self, *args, **kwargs):
        # Todo Next
        self.create_code()
        self.create_name()
        super(Curriculum, self).save(*args, **kwargs)

    def get_summary(self):
        return Curriculum.objects.get_with_summary().get(pk=self.id)

    def get_courses_by_semester(self):
        """
        semester_list = [
            {
                semester: 1,
                total_course: 3,
                total_sks: 24
                semester_courses: [CourseObject1 ... CourseObjectn],
            }
        ]
        """
        curriculum_courses = getattr(self, 'curriculum_courses', None)
        semester = []
        semester_list = []
        for course in curriculum_courses.all():
            if course.semester_number not in semester:
                semester.append(course.semester_number)
        for sms in semester:
            current_courses = curriculum_courses.filter(semester_number=sms)
            semester_list.append({
                'semester': sms,
                'course_count': len(current_courses.values('id')),
                'sks_meeting': sum(map(lambda x: x.sks_meeting, current_courses)),
                'sks_practice': sum(map(lambda x: x.sks_practice, current_courses)),
                'sks_field_practice': sum(map(lambda x: x.sks_field_practice, current_courses)),
                'sks_simulation': sum(map(lambda x: x.sks_simulation, current_courses)),
                'sks_total': sum(map(lambda x: x.sks_total, current_courses)),
                'semester_courses': current_courses.all()
            })
        return semester_list


class CurriculumCourse(Orderable, CurriculumCourseAbstract):
    class Meta:
        verbose_name = _("curricullum course")
        verbose_name_plural = _("curricullum courses")
        unique_together = ('curriculum', 'course')
        ordering = ('curriculum', 'semester_number',)

    objects = CurricullumCourseManager()

    curriculum = ParentalKey(
        Curriculum, on_delete=models.CASCADE,
        related_name='curriculum_courses',
        verbose_name=_("curriculum"))
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        related_name='curriculum_courses',
        verbose_name=_("course"))

    # wagtail autocomplete
    autocomplete_search_field = 'course__name'

    def autocomplete_label(self):
        return "{} | {} SKS | {}".format(self.curriculum.code, self.sks_total, self.course)

    def __str__(self):
        return self.course.name

    def save(self, *args, **kwargs):
        self.sks_total = (
            self.sks_meeting
            + self.sks_practice
            + self.sks_field_practice
            + self.sks_simulation
        )
        super().save(*args, **kwargs)


class CourseEqualizer(ClusterableModel, CourseEqualizerAbstract):
    class Meta:
        verbose_name = _("course equalizer")
        verbose_name_plural = _("course equalizers")
        unique_together = ('old_course', 'new_course')

    old_course = models.ForeignKey(
        CurriculumCourse,
        on_delete=models.PROTECT,
        related_name='old_equalizers',
        verbose_name=_('old course'))
    new_course = models.ForeignKey(
        CurriculumCourse,
        on_delete=models.PROTECT,
        related_name='new_equalizers',
        verbose_name=_('New Course'))

    def __str__(self):
        return "{}-{}".format(self.old_course, self.new_course)
