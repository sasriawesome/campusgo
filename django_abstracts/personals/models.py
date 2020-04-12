from django.db import models
from django.utils import translation, timezone
from django.utils.functional import cached_property
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from django_abstracts.core.enums import MaxLength, ActiveStatus
from django_abstracts.personals.enums import (
    Gender, EducationStatus, WorkingStatus, FamilyRelation
)

_ = translation.gettext_lazy


class ContactAbstract(models.Model):
    class Meta:
        abstract = True

    phone = models.CharField(
        max_length=MaxLength.SHORT.value,
        null=True, blank=True,
        verbose_name=_('phone'))
    fax = models.CharField(
        max_length=MaxLength.SHORT.value,
        null=True, blank=True,
        verbose_name=_('fax'))
    whatsapp = models.CharField(
        max_length=MaxLength.SHORT.value,
        null=True, blank=True,
        verbose_name=_('whatsapp'))
    email = models.EmailField(
        max_length=MaxLength.SHORT.value,
        null=True, blank=True,
        verbose_name=_('email'))
    website = models.CharField(
        max_length=MaxLength.SHORT.value,
        null=True, blank=True,
        verbose_name=_('website'))


class SocialAbstract(models.Model):
    class Meta:
        abstract = True

    # Social Media
    facebook = models.URLField(
        null=True, blank=True,
        help_text=_('Facebook page URL'))
    twitter = models.CharField(
        null=True, blank=True,
        max_length=255,
        help_text=_('Twitter username, without the @'))
    instagram = models.CharField(
        null=True, blank=True,
        max_length=255,
        help_text=_('Instagram username, without the @'))
    youtube = models.URLField(
        null=True, blank=True,
        help_text=_('Youtube channel or user account URL'))


class AddressAbstract(models.Model):
    class Meta:
        abstract = True

    is_primary = models.BooleanField(
        default=True, verbose_name=_('primary'))
    name = models.CharField(
        null=True, blank=False,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("name"),
        help_text=_('E.g. Home Address or Office Address'))
    street = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.LONG.value,
        verbose_name=_('street'))
    city = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('city'))
    province = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('province'))
    country = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('country'))
    zipcode = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('zip code'))

    def __str__(self):
        return self.street

    @property
    def fulladdress(self):
        address = [self.street, self.city, self.province, self.country, self.zipcode]
        return ", ".join(map(str, address))


class TitleMixin(models.Model):
    class Meta:
        abstract = True

    fullname = NotImplemented

    show_title = models.BooleanField(
        default=False,
        verbose_name=_('show title'),
        help_text=_('Show Mr or Mrs in front of name'))
    show_name_only = models.BooleanField(
        default=False,
        verbose_name=_('show name only'),
        help_text=_('Show name only without academic title'))
    title = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("title"))
    front_title = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("front title"),
        help_text=_("Academic title prefix, eg: Dr or Prof. Dr"))
    back_title = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("back title"),
        help_text=_("Academic title suffix, eg: Phd"))

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


class PersonAbstract(models.Model):
    class Meta:
        abstract = True

    pid = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("PID"),
        help_text=_('Personal Identifier Number'))
    fullname = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("full name"))
    nickname = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("nick name"))

    gender = models.CharField(
        max_length=1,
        choices=Gender.CHOICES.value,
        default=Gender.MALE.value,
        verbose_name=_('gender'))
    religion = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('religion'))
    nation = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('nation'))
    date_of_birth = models.DateField(
        null=True, blank=True,
        default=timezone.now,
        verbose_name=_('date of birth'))
    place_of_birth = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('place of birth'))

    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        related_name='person',
        on_delete=models.CASCADE,
        verbose_name=_('User account'))

    def __str__(self):
        return self.fullname

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @cached_property
    def is_user(self):
        user = self.account
        return bool(user)


class HistoryBase(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(
        max_length=50,
        verbose_name=_('name'))
    institution = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("institution"))
    date_start = models.DateField(
        default=timezone.now,
        verbose_name=_("date start"))
    date_end = models.DateField(
        default=timezone.now,
        verbose_name=_("date end"))
    status = models.CharField(
        max_length=5,
        default=EducationStatus.ONGOING.value,
        choices=EducationStatus.CHOICES.value,
        verbose_name=_("current status"))
    document_link = models.URLField(
        null=True, blank=True,
        verbose_name=_('document link'),
        help_text=_('Provide support document link'))

    def __str__(self):
        return self.name


class FormalEduAbstract(HistoryBase):
    class Meta:
        abstract = True

    major = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        null=True, blank=True,
        verbose_name=_("major"),
        help_text=_("ex: Information System or Accounting"))


class NonFormalEduAbstract(HistoryBase):
    class Meta:
        abstract = True

    description = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        null=True, blank=True,
        verbose_name=_("description"))


class WorkingAbstract(HistoryBase):
    class Meta:
        abstract = True

    department = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("department"))
    position = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("position"))
    description = models.TextField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("description"))
    employment = models.CharField(
        max_length=5,
        default=WorkingStatus.CONTRACT.value,
        choices=WorkingStatus.CHOICES.value,
        verbose_name=_("employment"))

    def __str__(self):
        return "%s, %s" % (self.institution, self.position)


class VolunteerAbstract(models.Model):
    class Meta:
        abstract = True

    organization = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("organization"))
    position = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("position"))
    description = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("description"))
    date_start = models.DateField(
        default=timezone.now,
        verbose_name=_("date start"))
    date_end = models.DateField(
        default=timezone.now,
        verbose_name=_("date end"))
    status = models.CharField(
        max_length=5,
        default=ActiveStatus.ACTIVE.value,
        choices=ActiveStatus.CHOICES.value,
        verbose_name=_("status"))
    document_link = models.URLField(
        null=True, blank=True,
        verbose_name=_('document link'),
        help_text=_('Provide support document link'))

    def __str__(self):
        return "%s, %s" % (self.organization, self.position)


class AwardAbstract(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("name"))
    description = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        null=True, blank=True,
        verbose_name=_("description"))
    date = models.DateTimeField(
        null=True, blank=True,
        default=timezone.now,
        verbose_name=_('created date'))
    document_link = models.URLField(
        null=True, blank=True,
        verbose_name=_('document link'),
        help_text=_('Provide support document link'))

    def __str__(self):
        return self.name


class SkillAbstract(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("name"))
    description = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        null=True, blank=True,
        verbose_name=_("description"))
    level = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ],
        verbose_name=_('Skill level'))

    def __str__(self):
        return self.name


class PublicationAbstract(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("title"))
    description = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        null=True, blank=True,
        verbose_name=_("description"))
    publisher = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        null=True, blank=True,
        verbose_name=_("publisher"))
    date_published = models.DateField(
        null=True, blank=True,
        default=timezone.now,
        verbose_name=_('published date'))
    document_link = models.URLField(
        null=True, blank=True,
        verbose_name=_('document link'),
        help_text=_('provide support document link'))

    def __str__(self):
        return self.title


class FamilyAbstract(models.Model):
    class Meta:
        abstract = True

    relation = models.PositiveIntegerField(
        choices=FamilyRelation.CHOICES.value,
        default=FamilyRelation.OTHER.value,
        verbose_name=_("relation"))
    relationship = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("other relation"))
    name = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("name"))
    date_of_birth = models.DateField(
        null=True, blank=True,
        default=timezone.now,
        verbose_name=_('date of birth'))
    place_of_birth = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('place of birth'))
    job = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("job"))
    address = models.TextField(
        max_length=MaxLength.LONG.value,
        null=True, blank=True,
        verbose_name=_("address"))

    def __str__(self):
        return self.name
