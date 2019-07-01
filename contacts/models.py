from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone_number    = PhoneNumberField()
    image           = models.ImageField(upload_to='image', null=True, blank=True)
    contacts         = models.ManyToManyField("Contact")

    def __str__(self):
        return self.username


class Contact(models.Model):
    first_name                  = models.CharField(max_length=128)
    last_name                   = models.CharField(max_length=128)
    phone_number                = PhoneNumberField()
    image                       = models.ImageField(upload_to='image', null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name