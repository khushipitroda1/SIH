from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

# class UserType(models.Model):
#     STUDENT = 1
#     TEACHER = 2
#     SECRETARY = 3
#     SUPERVISOR = 4
#     ADMIN = 5
#     ROLE_CHOICES = (
#         (STUDENT, 'student'),
#         (TEACHER, 'teacher'),
#         (SECRETARY, 'secretary'),
#         (SUPERVISOR, 'supervisor'),
#         (ADMIN, 'admin'),
#     )

#     id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

#     def str(self):
#         return self.get_id_display()

class CustomUser(AbstractUser,PermissionsMixin):
    
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    mobile = models.CharField(max_length=14)

    USER_TYPE_CHOICES = (
      ('health', 'health'),
      ('political', 'political'),
      ('sports', 'sports'),
      ('tourism', 'tourism'),
      ('education', 'education'),
  )

    user_type = models.CharField(choices=USER_TYPE_CHOICES  ,default="None", max_length=50)

    # user_type = models.ManyToManyField(UserType)
    object = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []