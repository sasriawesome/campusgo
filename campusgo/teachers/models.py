from django.db import models
from django.utils import translation

from campusgo.core.models import BaseModel, MaxLength
from campusgo.persons.models import Person, PersonManager
from campusgo.academic.models import Course, ResourceManagementUnit

_ = translation.gettext_lazy


class TeacherPersonalManager(PersonManager):
    def get_queryset(self):
        return super().get_queryset().filter(
            models.Q(teacher__isnull=False) | models.Q(is_teacher_applicant=True)
        ).prefetch_related('employee')


class TeacherPersonal(Person):
    class Meta:
        verbose_name = _('Teacher Personal')
        verbose_name_plural = _('Teacher Personals')
        proxy = True

    objects = TeacherPersonalManager()

    @property
    def is_employee(self):
        return bool(getattr(self, 'employee', False))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class TeacherManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('person')

    def get_by_natural_key(self, tid):
        return self.get(tid=tid)


class Teacher(BaseModel):
    class Meta:
        verbose_name = _('Teacher')
        verbose_name_plural = _('Teachers')

    objects = TeacherManager()
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE,
        verbose_name=_("Person"))
    tid = models.CharField(
        unique=True, null=True, blank=True,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('Teacher ID'))
    rmu = models.ForeignKey(
        ResourceManagementUnit, on_delete=models.PROTECT,
        related_name='teachers',
        verbose_name=_('Homebase'))
    courses = models.ManyToManyField(
        Course, verbose_name=_('Courses'))
    is_active = models.BooleanField(
        default=True, verbose_name=_("Active status"))

    # wagtail autocomplete
    autocomplete_search_field = 'employee__person__fullname'

    def autocomplete_label(self):
        return "{} | {}".format(self.employee.eid, self.name)

    def __str__(self):
        return self.person.fullname

    @property
    def name(self):
        return self.person.fullname

    def natural_key(self):
        natural_key = (self.tid,)
        return natural_key
