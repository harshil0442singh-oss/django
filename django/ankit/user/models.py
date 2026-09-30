from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserDetailsManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_admin(email, password, **extra_fields)


class UserDetails(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    mobile_number = models.BigIntegerField(unique=True)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Recruiter fields
    designation = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    about_company = models.TextField(null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)

    # Seeker fields
    address = models.TextField(null=True, blank=True)
    course = models.CharField(max_length=255, null=True, blank=True)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    # specialisation = models.CharField(max_length=255, null=True, blank=True)
    course_type = models.CharField(max_length=100, null=True, blank=True)
    college = models.CharField(max_length=255, null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    year_of_passing = models.IntegerField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    experience_level = models.CharField(max_length=100, null=True, blank=True)
    responsibilities = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    worked_from = models.DateField(null=True, blank=True)
    to = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile_number']

    objects = UserDetailsManager()

    def __str__(self):
        return self.email
