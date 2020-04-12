from django.db import models
from django.utils import translation

from django_abstracts.core.enums import MaxLength
from django_abstracts.core.models import BaseModel
from campusgo.persons.models import Person, PersonManager
from campusgo.academic.models import Course, ManagementUnit

_ = translation.gettext_lazy


class TeacherPersonalManager(PersonManager):
    def get_queryset(self):
        return super().get_queryset().filter(
            models.Q(teacher__isnull=False) | models.Q(is_teacher_applicant=True)
        )


class TeacherPersonal(Person):
    class Meta:
        verbose_name = _('teacher personal')
        verbose_name_plural = _('teacher personals')
        proxy = True

    objects = TeacherPersonalManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class TeacherManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('person')

    def get_by_natural_key(self, tid):
        return self.get(tid=tid)


class Teacher(BaseModel):
    class Meta:
        verbose_name = _('teacher')
        verbose_name_plural = _('teachers')

    objects = TeacherManager()
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE,
        verbose_name=_("person"))
    tid = models.CharField(
        unique=True, null=True, blank=True,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('teacher ID'))
    rmu = models.ForeignKey(
        ManagementUnit, on_delete=models.PROTECT,
        related_name='teachers',
        verbose_name=_('management unit'),
        help_text=_("Teacher homebase."))
    courses = models.ManyToManyField(
        Course, verbose_name=_('courses'))
    is_active = models.BooleanField(
        default=True, verbose_name=_("active status"))

    # wagtail autocomplete
    autocomplete_search_field = 'person__fullname'

    def autocomplete_label(self):
        return "{}".format(self.person.fullname)

    def __str__(self):
        return self.person.fullname

    @property
    def name(self):
        return self.person.fullname

    def natural_key(self):
        natural_key = (self.tid,)
        return natural_key
