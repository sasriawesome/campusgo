import uuid
import enum
from django.utils import translation
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group

from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.models import Image
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, FieldPanel, MultiFieldPanel

from modelcluster.models import ClusterableModel, get_all_child_m2m_relations, get_all_child_relations

_ = translation.gettext_lazy


class MaxLength(enum.Enum):
    SHORT = 128
    MEDIUM = 256
    LONG = 512
    XLONG = 1024
    TEXT = 2048
    RICHTEXT = 10000


class BaseManager(models.Manager):
    """
        Implement paranoid mechanism queryset
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def get(self, *args, **kwargs):
        kwargs['is_deleted'] = False
        return super().get(*args, **kwargs)


class BaseModel(models.Model):
    class Meta:
        abstract = True

    objects = BaseManager()

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name='uuid')
    is_deleted = models.BooleanField(
        default=False,
        editable=False,
        verbose_name=_('is deleted?'))
    deleted_by = models.ForeignKey(
        get_user_model(),
        editable=False,
        null=True, blank=True,
        related_name="%(class)s_deleter",
        on_delete=models.CASCADE,
        verbose_name=_('deleter'))
    deleted_at = models.DateTimeField(
        null=True, blank=True, editable=False)
    created_by = models.ForeignKey(
        get_user_model(),
        editable=False,
        null=True, blank=True,
        related_name="%(class)s_creator",
        on_delete=models.CASCADE,
        verbose_name=_('creator'))
    created_at = models.DateTimeField(
        default=timezone.now, editable=False)
    modified_at = models.DateTimeField(
        null=True, blank=True, editable=False)

    def save(self, **kwargs):
        self.modified_at = timezone.now()
        super().save(**kwargs)

    def delete(self, using=None, keep_parents=False, paranoid=False):
        """
            Give paranoid delete mechanism to each record
        """
        if paranoid:
            self.is_deleted = True
            self.deleted_at = timezone.now()
            self.save()
        else:
            super().delete(using=using, keep_parents=keep_parents)


class SignalAwareClusterableModel(ClusterableModel):
    class Meta:
        abstract = True

    def save(self, commit_childs=True, **kwargs):
        """
        Save the model and commit all child relations.
        """
        child_relation_names = [rel.get_accessor_name() for rel in get_all_child_relations(self)]
        child_m2m_field_names = [field.name for field in get_all_child_m2m_relations(self)]

        update_fields = kwargs.pop('update_fields', None)

        if update_fields is None:
            real_update_fields = None
            relations_to_commit = child_relation_names
            m2m_fields_to_commit = child_m2m_field_names
        else:
            real_update_fields = []
            relations_to_commit = []
            m2m_fields_to_commit = []
            for field in update_fields:
                if field in child_relation_names:
                    relations_to_commit.append(field)
                elif field in child_m2m_field_names:
                    m2m_fields_to_commit.append(field)
                else:
                    real_update_fields.append(field)

        super(ClusterableModel, self).save(update_fields=real_update_fields, **kwargs)

        # Skip commit, when post_save using signal
        if commit_childs:
            for relation in relations_to_commit:
                getattr(self, relation).commit()

            for field in m2m_fields_to_commit:
                getattr(self, field).commit()


class CampusGoSetting(BaseSetting):
    class Meta:
        verbose_name = _('General')
        verbose_name_plural = _('General')

    menu_icon = 'tag'

    fiscal_default = timezone.make_aware(
        timezone.datetime(timezone.now().year, 1, 1, 0, 0, 0))

    fiscal_year_start = models.DateField(
        default=fiscal_default, verbose_name=_('Fiscal year start'))
    fiscal_year_end = models.DateField(
        default=timezone.now, verbose_name=_('Fiscal year end'))

    logo = models.ForeignKey(
        Image, null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Logo'),
        help_text=_('Your company Logo (square, transparent baground is better)'))
    name = models.CharField(
        null=True, blank=True,
        max_length=255, help_text=_('Your company name'))
    tagline = models.CharField(
        null=True, blank=True,
        max_length=255, help_text=_('Your company tagline'))
    website = models.CharField(
        null=True, blank=True,
        max_length=255, help_text=_('Website URL.'))
    sitename = models.CharField(
        null=True, blank=True,
        max_length=255, help_text=_('Site name, widely used in this site.'))

    street1 = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('Address 1'))
    street2 = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('Address 2'))
    city = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('City'))
    province = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('Province'))
    country = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('Country'))
    zipcode = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name=_('Zip Code'))

    phone = models.CharField(
        null=True, blank=True,
        max_length=255, help_text=_('Phone number @'))
    fax = models.CharField(
        null=True, blank=True,
        max_length=255, help_text=_('Fax number @'))
    email = models.EmailField(
        null=True, blank=True,
        max_length=255, help_text=_('Valid email'))
    facebook = models.URLField(
        null=True, blank=True,
        help_text=_('Facebook page URL'))
    twitter = models.CharField(
        null=True, blank=True,
        max_length=255, help_text=_('twitter username, without the @'))
    instagram = models.CharField(
        null=True, blank=True,
        max_length=255, help_text=_('Instagram username, without the @'))
    youtube = models.URLField(
        null=True, blank=True,
        help_text=_('YouTube channel or user account URL'))

    # Account Settings ================================================

    user_registration_enabled = models.BooleanField(
        default=True, verbose_name=_('User registration enabled'),
        help_text=_('Activate user registration form'))
    default_new_user_group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name=_('Registration default group'),
        help_text=_('Include new registered user to this group'))
    auto_create_person = models.BooleanField(
        default=True, verbose_name=_('Auto create person'),
        help_text=_('Create person data for new user created'))

    # All Auth Setting =================================================

    login_with_twitter = models.BooleanField(
        default=True, verbose_name=_('Login with Twitter'),
        help_text=_('Activate login with Twitter'))
    login_with_facebook = models.BooleanField(
        default=True, verbose_name=_('Login with Facebook'),
        help_text=_('Activate login with Facebook'))
    login_with_google = models.BooleanField(
        default=True, verbose_name=_('Login with Google'),
        help_text=_('Activate login with Google'))
    login_with_github = models.BooleanField(
        default=True, verbose_name=_('Login with Github'),
        help_text=_('Activate login with Github'))
    login_with_slack = models.BooleanField(
        default=True, verbose_name=_('Login with Slack'),
        help_text=_('Activate login with Slack'))

    basic_panels = [
        MultiFieldPanel([
            ImageChooserPanel('logo'),
            FieldPanel('name'),
            FieldPanel('tagline'),
            FieldPanel('website'),
            FieldPanel('sitename'),
        ])
    ]

    contact_panels = [
        MultiFieldPanel([
            FieldPanel('street1'),
            FieldPanel('street2'),
            FieldPanel('city'),
            FieldPanel('province'),
            FieldPanel('country'),
            FieldPanel('zipcode'),
        ], heading=_('Address')),
        MultiFieldPanel([
            FieldPanel('phone'),
            FieldPanel('fax'),
            FieldPanel('email')
        ], heading=_('Contacts')),
        MultiFieldPanel([
            FieldPanel('facebook'),
            FieldPanel('twitter'),
            FieldPanel('instagram'),
            FieldPanel('youtube'),
        ], heading=_('Social Accounts'))
    ]

    misc_panels = [
        MultiFieldPanel([
            FieldPanel('fiscal_year_start'),
            FieldPanel('fiscal_year_end'),
        ])
    ]

    accounts_panels = [
        MultiFieldPanel([
            FieldPanel('user_registration_enabled'),
            FieldPanel('default_new_user_group'),
            FieldPanel('auto_create_person'),
        ], heading=_('Registration')),
        MultiFieldPanel([
            FieldPanel('login_with_twitter'),
            FieldPanel('login_with_facebook'),
            FieldPanel('login_with_google'),
            FieldPanel('login_with_github'),
            FieldPanel('login_with_slack'),
        ], heading=_('Registration'))
    ]

    edit_handler = TabbedInterface([
        ObjectList(basic_panels, heading=_('Basic')),
        ObjectList(contact_panels, heading=_('Contact')),
        ObjectList(accounts_panels, heading=_('Account')),
        ObjectList(misc_panels, heading=_('Misc'))
    ])

    @property
    def full_address(self):
        line1 = []
        if self.street1:
            line1.append(self.street1)
        if self.street2:
            line1.append(self.street2)

        line2 = []
        if self.zipcode:
            line2.append(self.city)
        if self.province:
            line2.append(self.province)
        if self.country:
            line2.append(self.country)
        if self.zipcode:
            line2.append(self.zipcode)

        line1 = " ".join(line1)
        line2 = ", ".join(line2)
        return line1, line2


register_setting(CampusGoSetting)