from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("must have user email")
        if not password:
            raise ValueError("must have user password")
        user = self.model(email=self.normalize_email(email), **extra_fields)  # name, role 정보
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_teacher(self, email, password, **extra_fields):
        # if not extra_fields.get("teacher_code") in teacher_code_list:
        #   raise ValueError("teacher_code is not valid")

        extra_fields.setdefault("role", 2)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("role") != 2:
            raise ValueError("Teacher must have teacher role")

        return self.create_user(email=email, password=password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        # if not extra_fields.get("admin_code") in admin_code_list:
        #   raise ValueError("admin_code is not valid")

        extra_fields.setdefault("role", 1)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("role") != 1:
            raise ValueError("Superuser must have Admin role")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    first_name = None
    last_login = None
    last_name = None
    username = None
    is_staff = None
    is_superuser = None
    groups = None
    user_permissions = None

    DEFAULT_ROLE_CHOICES = ((1, "admin"), (2, "teacher"), (3, "student"))

    ROLE_CHOICES = getattr(settings, "ROLE_CHOICES", DEFAULT_ROLE_CHOICES)

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=3)

    objects = UserManager()

    uid = models.CharField(_("user id"), max_length=150, unique=True, primary_key=True)

    name = models.CharField(
        _("username"),
        max_length=150,
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        default="unknown",
    )
    email = models.EmailField(_("email address"), unique=True, max_length=128)

    USERNAME_FIELD = "uid"

    class Meta:
        db_table = u"User"

    REQUIRED_FIELDS = []
