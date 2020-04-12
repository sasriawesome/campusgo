from django.db import models
from django.utils import translation
from django.core.validators import MaxValueValidator, MinValueValidator
from mptt.models import MPTTModel, TreeForeignKey
from django_numerators.models import NumeratorMixin, NumeratorReset

from django_abstracts.core.enums import MaxLength
from django_abstracts.core.models import BaseModel
from .enums import ManagementLevel, Semester, KKNILevel, StudentStatus

_ = translation.gettext_lazy


class ManagementUnitAbstract(MPTTModel, BaseModel):
    class Meta:
        abstract = True

    type = models.IntegerField(
        default=ManagementLevel.UNIVERSITY.value,
        choices=ManagementLevel.CHOICES.value,
        verbose_name=_("type"))
    parent = TreeForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='childrens',
        verbose_name=_('parent'))
    code = models.SlugField(
        unique=True,
        max_length=3,
        verbose_name=_("code"))
    name = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("name"))


class SchoolYearAbstract(BaseModel):
    class Meta:
        abstract = True

    code = models.CharField(
        unique=True, editable=False,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("code"))
    year_start = models.IntegerField(
        choices=[(x, str(x)) for x in range(2010, 2030)],
        default=2019,
        verbose_name=_("year start"))
    year_end = models.IntegerField(
        choices=[(x, str(x)) for x in range(2010, 2030)],
        default=2020,
        verbose_name=_("year end"))


class AcademicYearAbstract(BaseModel):
    """
    Implement:
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.PROTECT,
        verbose_name=_("school year")
    )
    """

    class Meta:
        abstract = True

    school_year = NotImplementedError
    code = models.CharField(
        unique=True, editable=False,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("code"))
    semester = models.PositiveIntegerField(
        default=Semester.ODD.value,
        choices=Semester.CHOICES.value,
        verbose_name=_('semester'))
    date_start = models.DateField(
        verbose_name=_("date start"))
    date_end = models.DateField(
        verbose_name=_("date end"))


class AcademicActivityAbstract(BaseModel):
    """
    Implement:
    school_year = models.ForeignKey(
        SchoolYear,
        on_delete=models.PROTECT,
        related_name='activities',
        verbose_name=_('academic year')
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name='activities',
        verbose_name=_('academic year')
    )
    """

    class Meta:
        abstract = True

    school_year = NotImplementedError
    academic_year = NotImplementedError

    date_start = models.DateField(
        verbose_name=_("date start"))
    date_end = models.DateField(
        verbose_name=_("date end"))
    activity = models.TextField(
        verbose_name=_("activity"))


class CourseTypeAbstract(BaseModel):
    class Meta:
        abstract = True

    code = models.PositiveIntegerField(
        unique=True, default=1,
        choices=[(x, str(x)) for x in range(1, 10)],
        verbose_name=_("code"))
    name = models.CharField(
        max_length=MaxLength.LONG.value,
        verbose_name=_("name"))
    alias = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.LONG.value,
        verbose_name=_("alias"))


class CourseGroupAbstract(BaseModel):
    class Meta:
        abstract = True

    code = models.PositiveIntegerField(
        unique=True, default=1,
        choices=[(x, str(x)) for x in range(1, 10)],
        verbose_name=_("Code"))
    name = models.CharField(
        max_length=MaxLength.LONG.value,
        verbose_name=_("Name"))
    alias = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.LONG.value,
        verbose_name=_("Alias"))


class CourseAbstract(NumeratorMixin, BaseModel):
    """
    Implement:
    course_type = models.ForeignKey(
        CourseType,
        on_delete=models.PROTECT,
        verbose_name=_("course type"))
    course_group = models.ForeignKey(
        CourseGroup,
        on_delete=models.PROTECT,
        verbose_name=_("course group"))
    """

    class Meta:
        abstract = True

    zero_fill = 2
    reset_mode = NumeratorReset.FIXED

    rmu = NotImplementedError
    course_type = NotImplementedError
    course_group = NotImplementedError

    old_code = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("old code"),
        help_text=_('Maintain legacy system data integrity'))
    name = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("name"))
    teaching_method = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("teaching method"))
    level = models.PositiveIntegerField(
        choices=KKNILevel.UNIVERSITY.value,
        default=KKNILevel.S1.value,
        verbose_name=_('level'))
    year_offered = models.PositiveIntegerField(
        choices=[(x, str(x)) for x in range(1, 5)], default=1,
        verbose_name=_('year offered'))
    description = models.TextField(
        null=True, blank=True,
        max_length=MaxLength.RICHTEXT.value,
        verbose_name=_("description"))
    has_lpu = models.BooleanField(
        default=True, verbose_name=_("has LPU"),
        help_text=_('Lecture Program Unit a.k.a SAP'))
    has_dictate = models.BooleanField(
        default=True, verbose_name=_("has dictate"))
    has_teaching_material = models.BooleanField(
        default=True, verbose_name=_("has teaching material"))
    has_practice_program = models.BooleanField(
        default=True, verbose_name=_("has practice program"))
    is_active = models.BooleanField(
        default=True, verbose_name=_("active status"))


class CoursePreRequisiteAbstract(BaseModel):
    """
    Implement:
    rmu = TreeForeignKey(
        ManagementUnit,
        on_delete=models.PROTECT,
        related_name='courses',
        verbose_name=_("Management Unit"),
        help_text=_("Management Unit")
    )
    course = models.ForeignKey(
        Course,
        related_name="course_prerequisites",
        on_delete=models.CASCADE,
        verbose_name=_("Course")
    )
    requisite = models.ForeignKey(
        Course, null=True, blank=True,
        related_name="prerequisites",
        on_delete=models.CASCADE,
        verbose_name=_("Requisite")
    )
    """

    class Meta:
        abstract = True

    SCORE = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    )
    course = NotImplementedError
    requisite = NotImplementedError
    score = models.CharField(
        max_length=2, default='C', choices=SCORE,
        verbose_name=_('min graduated score'))


class CurriculumAbstract(BaseModel):
    """
    Implementation:
    rmu = TreeForeignKey(
        ManagementUnit,
        limit_choices_to={},
        on_delete=models.PROTECT,
        related_name='curriculums',
        verbose_name=_("Program Study"),
        help_text=_("Management Unit")
        )
    """

    class Meta:
        abstract = True

    rmu = NotImplementedError

    code = models.CharField(
        unique=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("code"))
    year = models.CharField(
        max_length=4,
        choices=[(str(x), str(x)) for x in range(2010, 2030)],
        default='2019',
        verbose_name=_("year"))
    name = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("name"))
    sks_graduate = models.PositiveIntegerField(
        default=0,
        verbose_name=_("SKS graduate"))
    is_active = models.BooleanField(
        default=True, verbose_name=_('Active'))


class CurriculumCourseAbstract(BaseModel):
    """
    Implemetation:
    curriculum = models.(
        Curriculum, on_delete=models.CASCADE,
        related_name='curriculum_courses',
        verbose_name=_("Curriculum")
        )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        related_name='course_curriculums',
        verbose_name=_("Course")
        )
    """

    class Meta:
        abstract = True
        unique_together = ('curriculum', 'course')
        ordering = ('curriculum', 'semester_number',)

    curriculum = NotImplementedError
    course = NotImplementedError

    semester_number = models.PositiveIntegerField(
        default=1,
        choices=[(x, str(x)) for x in range(1, 9)],
        verbose_name=_('semester'))
    semester_type = models.PositiveIntegerField(
        default=Semester.ODD,
        choices=Semester.CHOICES.value,
        verbose_name=_('Semester Type'))
    sks_meeting = models.PositiveIntegerField(
        default=0, verbose_name=_("SKS meeting"))
    sks_practice = models.PositiveIntegerField(
        default=0, verbose_name=_("SKS practice"))
    sks_field_practice = models.PositiveIntegerField(
        default=0, verbose_name=_("SKS field"))
    sks_simulation = models.PositiveIntegerField(
        default=0, verbose_name=_("SKS simulation"))
    sks_total = models.PositiveIntegerField(
        editable=False, default=0,
        verbose_name=_("SKS total"))


class CourseEqualizerAbstract(BaseModel):
    """
    Implement:
    old_course = models.ForeignKey(
        CurriculumCourse,
        on_delete=models.PROTECT,
        related_name='old_courses',
        verbose_name=_('Old Course')
    )
    new_course = models.ForeignKey(
        CurriculumCourse,
        on_delete=models.PROTECT,
        related_name='new_courses',
        verbose_name=_('New course')
    )
    """

    class Meta:
        abstract = True
        unique_together = ('old_course', 'new_course')

    sks_old_course = models.IntegerField(
        verbose_name=_('SKS old'))

    old_course = NotImplementedError
    new_course = NotImplementedError
    sks_new_course = models.IntegerField(
        verbose_name=_('SKS new'))

    def __str__(self):
        return "{}-{}".format(self.old_course, self.new_course)


class SyllabusAbstract(NumeratorMixin, BaseModel):
    """
    Implement:
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        related_name='syllabuses',
        verbose_name=_('course')
    )
    """

    class Meta:
        abstract = True

    reset_mode = NumeratorReset.FIXED
    title = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('name'))

    course = NotImplementedError
    description = models.TextField(
        max_length=MaxLength.RICHTEXT.value,
        verbose_name=_('description'))


class LectureProgramAbstract(NumeratorMixin, BaseModel):
    """
    Implement:
    syllabus = models.ForeignKey(
        Syllabus, on_delete=models.CASCADE,
        related_name='lecture_programs',
        verbose_name=_('syllabus')
    )
    """

    class Meta:
        abstract = True

    reset_mode = NumeratorReset.FIXED
    syllabus = NotImplementedError


class StudentAbstract(NumeratorMixin, BaseModel):
    """
    Implement:
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE,
        verbose_name=_("Person")
    )
    year_of_force = models.ForeignKey(
        SchoolYear, on_delete=models.PROTECT,
        verbose_name=_("year of force")
    )
    coach = models.ForeignKey(
        Teacher, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='students',
        verbose_name=_('coach')
    )
    rmu = models.ForeignKey(
        ManagementUnit,
        limit_choices_to={
            'type': ManagementLevel.PROGRAM_STUDY.value
        },
        on_delete=models.PROTECT,
        verbose_name=_('rogram study')
    )
    """

    class Meta:
        abstract = True

    zero_fill = 4
    reset_mode = NumeratorReset.FIXED

    person = NotImplementedError
    year_of_force = NotImplementedError
    coach = NotImplementedError
    rmu = NotImplementedError

    student_id = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('old student ID'))
    status = models.CharField(
        choices=StudentStatus.STATUS.value,
        default=StudentStatus.ACTIVE.value,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('Status'))
    status_note = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('status note'))
    registration_id = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name=_("registration ID"))
    registration = models.CharField(
        max_length=2, default='1',
        choices=(('1', 'reguler'), ('P', 'transfer')),
        verbose_name=_("registration"))


class StudentScoreAbstract(BaseModel):
    """
    Implement:
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        related_name='scores',
        verbose_name=_("Student"))
    course = models.ForeignKey(
        CurriculumCourse,
        on_delete=models.PROTECT,
        related_name='student_scores',
        verbose_name=_('Course'))
    """

    class Meta:
        abstract = True

    course = NotImplementedError
    student = NotImplementedError
    numeric = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name=_("numeric Score"))
    alphabetic = models.CharField(
        max_length=1,
        verbose_name=_("alphabetic Score"))


class ConversionScoreAbstract(models.Model):
    class Meta:
        abstract = True

    ori_code = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name=_('origin code'))
    ori_name = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name=_('origin name'))
    ori_numeric_score = models.DecimalField(
        default=1,
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4),
        ],
        verbose_name=_('origin numeric'))
    ori_alphabetic_score = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name=_('origin alphabetic'))


class Teacher(NumeratorMixin):
    """
    Implement:
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE,
        verbose_name=_("Person")
        )
    rmu = models.ForeignKey(
        ManagementUnit, on_delete=models.PROTECT,
        related_name='teachers',
        verbose_name=_('Homebase')
    )
    courses = models.ManyToManyField(
        Course, verbose_name=_('Courses')
    )
    """

    class Meta:
        abstract = True

    person = NotImplementedError
    rmu = NotImplementedError
    courses = NotImplementedError

    teacher_id = models.CharField(
        unique=True, null=True, blank=True,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('teacher ID'))
    is_active = models.BooleanField(
        default=True, verbose_name=_("active status"))
