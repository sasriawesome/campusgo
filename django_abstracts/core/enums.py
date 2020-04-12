import enum
from django.utils.translation import ugettext_lazy as _


class MaxLength(enum.Enum):
    SHORT = 128
    MEDIUM = 256
    LONG = 512
    XLONG = 1024
    TEXT = 2048
    RICHTEXT = 10000


class ActiveStatus(enum.Enum):
    ACTIVE = 'ACT'
    INACTIVE = 'INC'

    CHOICES = (
        (ACTIVE, _("active").title()),
        (INACTIVE, _("inactive").title()),
    )
