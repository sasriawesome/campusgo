from django.db import models
from django.utils import translation

from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable
from modelcluster.models import ParentalKey
from model_utils.fields import StatusField, MonitorField
from model_utils import Choices

from campusgo.core.models import BaseModel, SignalAwareClusterableModel, MaxLength
from campusgo.numerators.models import NumeratorMixin
from campusgo.academic.models import ResourceManagementUnit

_ = translation.gettext_lazy


class Program(SignalAwareClusterableModel, NumeratorMixin, BaseModel):
    class Meta:
        verbose_name = _('Program')
        verbose_name_plural = _('Programs')

    doc_code = 'MTR'
    title = models.CharField(
        max_length=MaxLength.LONG.value,
        verbose_name=_('Name'))
    description = RichTextField(
        max_length=MaxLength.RICHTEXT.value,
        verbose_name=_('Description'))
    program_study = models.ForeignKey(
        ResourceManagementUnit, on_delete=models.CASCADE,
        verbose_name=_('Program Study'))
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is active?'))

    def __str__(self):
        return self.title


class Price(Orderable, BaseModel):
    class Meta:
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')

    program = ParentalKey(
        Program, on_delete=models.CASCADE,
        related_name='prices',
        verbose_name=_('Program'))
    name = models.CharField(
        max_length=MaxLength.LONG.value,
        verbose_name=_('Name'))
    note = models.CharField(
        max_length=MaxLength.RICHTEXT.value,
        verbose_name=_('Note'))
    price = models.DecimalField(
        default=0.00,
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Price')
    )
    def __str__(self):
        return self.name


class Registration(NumeratorMixin, BaseModel):
    class Meta:
        verbose_name = _('Matriculant')
        verbose_name_plural = _('Matriculants')

    STATUS = Choices('draft', 'submitted')

    doc_code = 'MTR'

    program = models.ForeignKey(
        Program, on_delete=models.CASCADE,
        verbose_name=_('Program Study'))
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is active?'))
    status = StatusField()
    status_changed = MonitorField(monitor='status')

    def __str__(self):
        return self.program