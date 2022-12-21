from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

# from multiselectfield import MultiSelectField
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=50,
        unique=True,
        help_text=_('Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=50, blank=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    phone_no = models.CharField(_('phone no'), max_length = 10, null=True, blank=True)
    
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_('Designates whether the user can login and change into this admin site.'),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
        ),
    )
    
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_("last login"), auto_now=True)

    # is_advisor = models.BooleanField(default=False)
    # is_learner = models.BooleanField(default=True)

    class Types(models.TextChoices):
        ADVISOR = 'advisor', 'ADVISOR'
        LEARNER = 'learner', 'LEARNER'

    # type = MultiSelectField(choices=Types.choices, null=True, blank=True, default=[])

    objects = UserManager()

    USERNAME_FIELD = 'username'
    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Advisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

