from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import os


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password,  **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(blank=True, null=True, max_length=512)
    last_name = models.CharField(blank=True, null=True, max_length=512)
    login_attemps = models.IntegerField(default=0, null=True, blank=True)
    login_attemp_fails_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add = True)
    modified_at = models.DateTimeField(auto_now = True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class UserEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, unique=True)
    primary = models.BooleanField(default=False)


def get_file_url(instance, filename):
    print(instance)
    return os.path.join('files', filename)


class UserFiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    files = models.ImageField(upload_to=get_file_url)

    def filename(self):
        return os.path.basename(self.files.name)


class FileComments(models.Model):
    files = models.ForeignKey(UserFiles, on_delete=models.CASCADE)
    comments =  models.CharField(max_length=512, blank=True, null=True)
    commented_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)