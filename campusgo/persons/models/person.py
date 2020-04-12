import uuid
from django.db import models, transaction
from django.db.utils import cached_property
from django.utils import translation, timezone, text
from django.conf import settings
from django_abstracts.personals.models import (
    TitleMixin, PersonAbstract, ContactAbstract, AddressAbstract, SocialAbstract,
    SkillAbstract, AwardAbstract, FormalEduAbstract, NonFormalEduAbstract, WorkingAbstract,
    VolunteerAbstract, PublicationAbstract, FamilyAbstract)
from django_abstracts.academics.enums import KKNILevel
from django_numerators.models import NumeratorMixin

from wagtail.core.models import Orderable
from modelcluster.models import ClusterableModel, ParentalKey

from campusgo.core.models import MaxLength

_ = translation.gettext_lazy


class PersonManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_employee(self):
        return self.filter(employee__isnull=False)

    def get_customer(self):
        return self.filter(partners__is_customer=True)

    def get_vendor(self):
        return self.filter(partners__is_vendor=True)


class Person(ClusterableModel, NumeratorMixin, TitleMixin, ContactAbstract, SocialAbstract, PersonAbstract):
    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        permissions = (
            ('export_person', 'Can export Person'),
            ('import_person', 'Can import Person'),
            ('change_status_person', 'Can change status Person')
        )

    objects = PersonManager()

    # Last Education
    last_education_level = models.CharField(
        max_length=5,
        choices=KKNILevel.CHOICES.value,
        default=KKNILevel.SMA.value,
        verbose_name=_('Level'))
    last_education_institution = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('Institution'))
    last_education_name = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('Major'))
    year_graduate = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('year graduate'))

    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('account'))

    is_employee_applicant = models.BooleanField(default=False, verbose_name=_('employee applicant'))
    is_partner_applicant = models.BooleanField(default=False, verbose_name=_('partner applicant'))
    is_teacher_applicant = models.BooleanField(default=False, verbose_name=_('teacher applicant'))
    is_matriculant = models.BooleanField(default=False, verbose_name=_('matriculant'))

    @cached_property
    def fullname_with_title(self):
        name = []
        if self.title and self.show_title:
            name.append(self.title)
        if self.front_title and not self.show_name_only:
            name.append(str(self.front_title) + '.')
        if self.fullname:
            name.append(self.fullname)
        if self.back_title and not self.show_name_only:
            name.append(', ' + str(self.back_title))
        return " ".join(name)

    def __str__(self):
        return str(self.fullname_with_title)

    def save(self, force_insert=False, force_update=False,
             using=None,
             update_fields=None):
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using, update_fields=update_fields)

    @cached_property
    def is_user(self):
        user = self.account
        return bool(user)

    @cached_property
    def is_employee(self):
        employee = getattr(self, 'employee', None)
        if employee:
            employee = employee.is_active
        return bool(employee)

    @cached_property
    def is_teacher(self):
        teacher = getattr(self, 'teacher', None)
        if teacher:
            teacher = teacher.is_active
        return bool(teacher)

    @cached_property
    def is_student(self):
        student = getattr(self, 'student', None)
        if student:
            student = student.is_active
        return bool(student)

    @cached_property
    def is_partner(self):
        partner = getattr(self, 'partner', None)
        if partner:
            partner = partner.is_active
        return bool(partner)

    @cached_property
    def is_customer(self):
        partner = getattr(self, 'partner', None)
        customer = None
        if partner:
            customer = partner.is_active and partner.is_customer
        return bool(customer)

    @cached_property
    def is_supplier(self):
        partner = getattr(self, 'partner', None)
        supplier = None
        if partner:
            supplier = partner.is_active and partner.is_supplier
        return bool(supplier)

    @cached_property
    def is_vendor(self):
        partner = getattr(self, 'partner', None)
        vendor = None
        if partner:
            vendor = partner.is_active and partner.is_vendor
        return bool(vendor)

    @cached_property
    def get_last_education_level_display(self):
        return KKNILevel(self.last_education_level).name

    def create_account(self, username=None, password=None):
        if not self.account:
            with transaction.atomic():
                usermodel = settings.AUTH_USER_MODEL
                username = username if username else text.slugify(
                    self.fullname)
                password = password if password else 'default_pwd'
                new_user = usermodel.objects.create_user(
                    username=username,
                    password=password,
                    is_staff=False
                )
                self.account = new_user
                self.save()

    def bind_account(self, user):
        with transaction.atomic():
            self.account = user
            self.save()


class PersonAddress(Orderable, AddressAbstract):
    person = ParentalKey(
        Person, on_delete=models.CASCADE,
        related_name='addresses'
    )


class Skill(Orderable, SkillAbstract):
    person = ParentalKey(
        Person, on_delete=models.CASCADE,
        related_name='skills'
    )


class Award(Orderable, AwardAbstract):
    person = ParentalKey(
        Person, on_delete=models.CASCADE,
        related_name='awards'
    )


class FormalEducation(Orderable, FormalEduAbstract):
    level = models.PositiveIntegerField(
        choices=KKNILevel.CHOICES.value,
        default=KKNILevel.S1.value,
        verbose_name=_('level'))
    person = ParentalKey(
        Person, on_delete=models.CASCADE,
        related_name='formal_educations'
    )


class NonFormalEducation(Orderable, NonFormalEduAbstract):
    person = ParentalKey(
        Person, on_delete=models.CASCADE,
        related_name='non_formal_educations'
    )


class Working(Orderable, WorkingAbstract):
    person = ParentalKey(
        Person, on_delete=models.CASCADE,
        related_name='work_histories'
    )


class Volunteer(Orderable, VolunteerAbstract):
    person = ParentalKey(
        Person, on_delete=models.CASCADE,
        related_name='volunteers'
    )


class Publication(Orderable, PublicationAbstract):
    person = ParentalKey(
        Person, on_delete=models.CASCADE,
        related_name='publications'
    )


class Family(Orderable, FamilyAbstract):
    person = ParentalKey(
        Person, on_delete=models.CASCADE,
        related_name='families'
    )
