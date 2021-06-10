from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(_("Subject"), max_length=100)
    message = models.TextField(_("Message"))
    read = models.BooleanField(default=False)
    timenow = models.DateTimeField(auto_now=True)

class Destinations(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    address = models.CharField(_("Address"), max_length=100)
    description = models.CharField(_("Description"), max_length=100)
    image = models.CharField(_("Image"), max_length=50)
    text = models.TextField(_("Text"))

class Tour(models.Model):
    destination = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datefrom = models.DateField(_("From"), auto_now=False, auto_now_add=False)
    dateto = models.DateField(_("To"), auto_now=False, auto_now_add=False)
    people = models.IntegerField(_("No of People"))
    read = models.BooleanField(default=False)
    arriving = models.BooleanField(default=False)
    leaving = models.BooleanField(default=False)
    timenow = models.DateTimeField(auto_now=True)
    approve = models.BooleanField(null=True, blank=True)

class Reply(models.Model):
    message = models.ForeignKey(Contact, on_delete=models.CASCADE)
    reply = models.TextField()
    read = models.BooleanField(default=False)