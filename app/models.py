from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Blood(models.Model):
    group = models.CharField(verbose_name=_("Blood Group"), max_length=10, unique=True, null=True, blank=True)
    stock = models.PositiveIntegerField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='blood')
    status = models.BooleanField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


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


class BloodRequest(models.Model):
    status = (
        ("Approved", "Approved"),
        ("Delivered", "Delivered"),
        ("Canceled", "Canceled"),
    )
    blood = models.ForeignKey(Blood, on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, blank=True)
    amount = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True, choices=status, default="Approved")

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class RequestToDonor(models.Model):
    from_patient = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, blank=True, related_name='From+')
    to_donor = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, blank=True, related_name='To+')
    blood = models.ForeignKey(Blood, on_delete=models.PROTECT, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Event(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    organized_by = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    event_date = models.DateField(null=True, blank=True)
    event_time = models.TimeField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='images')
    event_dt = models.DateTimeField(null=True, blank=True)
    registration = models.PositiveIntegerField(null=True, blank=True, default=0)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, blank=True)
    donation_status = models.BooleanField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name=_("User Name"), null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    like = models.PositiveIntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class FeedbackLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name=_("User Name"), null=True, blank=True)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class ContactForm(models.Model):
    name = models.CharField(verbose_name=_("Sender Name"), max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)