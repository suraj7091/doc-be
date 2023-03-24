from enum import Enum
from datetime import date

from django.db import models
from django.contrib.auth.models import User

from organizations.models import Organization


class GenderType(Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_rel')
    organization = models.OneToOneField(Organization, on_delete=models.PROTECT, related_name='user_organization')
    mobile = models.CharField(max_length=12, blank=True, null=True, default='')
    dob = models.DateField(blank=True, null=True, default=date.today())
    gender = models.CharField(max_length=255, choices=GenderType.choices(), default='Male')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_profile'
