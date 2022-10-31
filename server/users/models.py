from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.management.utils import get_random_secret_key
from django.contrib.auth.mixins import PermissionsMixin


class UserCustomManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError('The given phonenumber must be set')
        user = self.model(phone_number=phone_number, username=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    secret_key = models.CharField(max_length=255, default=get_random_secret_key)
    username = None


    first_name = models.CharField(max_length=150,blank=False)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserCustomManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'first_name']

    def __str__(self):
        return self.first_name


# class User(AbstractUser):
#     username = None

#     email = models.EmailField(unique=True, db_index=True)
#     secret_key = models.CharField(max_length=255, default=get_random_secret_key)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     class Meta:
#         swappable = 'AUTH_USER_MODEL'

#     @property
#     def name(self):
#         if not self.last_name:
#             return self.first_name.capitalize()

#         return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'
