from django.db import models
from django.utils.encoding import force_bytes
from django.contrib.auth.models import AbstractUser
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from app_modules.base.utils import normalize_email

class CustomManager(models.Manager):

    """
    Custom manager for filtering objects based on their status.

    This manager provides custom methods to filter model instances based on
    their `status` field. It includes methods for getting all active instances
    and filtering active instances with additional criteria.
    """

    def active_all(self):
        return super().get_queryset().filter(status='Active')
    
    def active_filter(self, **kwargs):
        return self.get_queryset().filter(status='Active', **kwargs)
    
    def get_by_natural_key(self, email):
        return self.get_queryset().get(email=email)
    
    def normalize_email(self,email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        return normalize_email(email)
        

class User(AbstractUser):

    """
    Custom User model that extends the default Django User model.

    This model adds additional fields for handling the user's role, 
    profile image, mobile number, and account status.
    """

    ACTIVE   = "Active"
    INACTIVE = "Inactive"

    STATUS_CHOICES = (
        (ACTIVE, ACTIVE),
        (INACTIVE, INACTIVE),
    )

    SUPER_ADMIN = "Super Admin"
    TEACHER     = "Teacher"
    STUDENT     = "Student"

    USER_ROLE = (
        (SUPER_ADMIN, SUPER_ADMIN),
        (TEACHER, TEACHER),
        (STUDENT, STUDENT),
    )

    email   = models.EmailField(_('Email'), unique=True)
    image   = models.ImageField(upload_to="users/profile pic/", null=True, blank=True)
    mobile  = models.CharField(_('Mobile'), max_length=15, null=True, blank=True)
    role    = models.CharField(_('Role'), choices=USER_ROLE, null=True, blank=True, max_length=100)
    status  = models.CharField(_('Status'), choices=STATUS_CHOICES, default=ACTIVE, max_length=100)
    objects = CustomManager()

    def __str__(self):
        return self.get_full_name().title() or self.username.title()
    
    def get_encoded_id(self):
        return urlsafe_base64_encode(force_bytes(self.pk))

class StudentManager(models.Manager):
    """
    Custom manager for filtering Student users.
    """
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.STUDENT)
    
    def normalize_email(self,email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        return normalize_email(email)

class Students(User):
    """
    Proxy model for the 'Student' user.
    """
    role    = User.STUDENT
    objects = StudentManager()

    class Meta:
        proxy = True
        verbose_name = 'Student'
        verbose_name_plural = 'Students'  

    def __str__(self):
        return self.get_full_name().title() or self.username.title()
    

class TeacherManager(models.Manager):
    """
    Custom manager for filtering Teacher users.
    """
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.TEACHER)
    
    def normalize_email(self,email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        return normalize_email(email)

class Teachers(User):
    """
    Proxy model for the 'Teacher' user.
    """
    role    = User.TEACHER
    objects = TeacherManager()

    class Meta:
        proxy = True
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'  

    def __str__(self):
        return self.get_full_name().title() or self.username.title()

class SAdminManager(models.Manager):
    """
    Custom manager for filtering Admin users.
    """
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.SUPER_ADMIN)
    
    def normalize_email(self,email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        return normalize_email(email)

class SuperAdmin(User):
    """
    Proxy model for the 'Super Admin' user.
    """
    role    = User.SUPER_ADMIN
    objects = SAdminManager()

    class Meta:
        proxy = True
        verbose_name = 'SuperAdmin'
        verbose_name_plural = 'SuperAdmins'  

    def __str__(self):
        return self.get_full_name().title() or self.username.title()