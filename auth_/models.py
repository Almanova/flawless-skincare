from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    PermissionsMixin, BaseUserManager

from mixin.models import BaseModel
from utils import constants, uploads


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, role, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        if not role:
            raise ValueError('The given role must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email,
                          role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, role, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, role, password, **extra_fields)

    def create_superuser(self, username, email, role, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, role, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(max_length=100,
                                unique=True,
                                db_index=True,
                                verbose_name='Username')
    email = models.EmailField(max_length=100,
                              unique=True,
                              db_index=True,
                              verbose_name='Email address')
    first_name = models.CharField(max_length=50,
                                  null=True,
                                  blank=True,
                                  verbose_name='First name')
    last_name = models.CharField(max_length=50,
                                 null=True,
                                 blank=True,
                                 verbose_name='Last name')
    phone = models.CharField(max_length=30,
                             null=True,
                             blank=True,
                             db_index=True,
                             verbose_name='Phone number')
    is_active = models.BooleanField(default=True,
                                    verbose_name='Active')
    is_staff = models.BooleanField(default=False,
                                   verbose_name='Staff account')
    role = models.CharField(choices=constants.ROLES,
                            default=constants.CUSTOMER,
                            max_length=30,
                            verbose_name='Role')
    confirmed = models.BooleanField(default=False,
                                    verbose_name='Confirmed account')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone', 'role']

    class Meta:
        ordering = ['-created']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def save(self, *args, **kwargs):
        BaseModel.save(self, *args, **kwargs)

    def delete(self, *args, **kwargs):
        BaseModel.delete(self, *args, **kwargs)


class CustomerProfile(BaseModel):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='User')
    city = models.CharField(max_length=50,
                            db_index=True,
                            blank=True,
                            null=True,
                            verbose_name='City')
    address = models.CharField(max_length=200,
                               db_index=True,
                               blank=True,
                               null=True,
                               verbose_name='Address')
    birth_date = models.DateField(blank=True,
                                  null=True,
                                  db_index=True,
                                  verbose_name='Birth date')
    avatar = models.FileField(upload_to=uploads.avatar_upload,
                              blank=True,
                              null=True,
                              verbose_name='User avatar')

    class Meta:
        verbose_name = 'Customer profile'
        verbose_name_plural = 'Customer profiles'


class AdminProfile(CustomerProfile):
    position = models.CharField(max_length=100,
                                db_index=True,
                                blank=True,
                                null=True,
                                verbose_name="Work position")

    class Meta:
        verbose_name = 'Admin profile'
        verbose_name_plural = 'Admin profiles'


class Brand(BaseModel):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='User')
    name = models.CharField(max_length=100,
                            db_index=True,
                            blank=True,
                            null=True,
                            verbose_name='Brand name')
    logo = models.FileField(upload_to=uploads.brand_logo_upload,
                            blank=True,
                            null=True,
                            verbose_name='Brand logo')
    description = models.TextField(max_length=500,
                                   blank=True,
                                   null=True,
                                   verbose_name='Description')

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
