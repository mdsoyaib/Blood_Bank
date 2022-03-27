from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Blood(models.Model):
    group = models.CharField(verbose_name=_("Blood Group"), max_length=10, unique=True, null=True, blank=True)
    stock = models.PositiveIntegerField(null=True, blank=True)
    status = models.BooleanField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.group


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, blank=True, unique=True, null=True)
    phone = models.CharField(verbose_name=_("Mobile phone"), max_length=14, blank=True, null=True, unique=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    blood = models.CharField(verbose_name=_("Blood Group"), max_length=10, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class City(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Event(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    organized_by = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    event_date = models.DateField(null=True, blank=True)
    event_time = models.TimeField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='images')
    event_dt = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, blank=True)
    donation_status = models.BooleanField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)