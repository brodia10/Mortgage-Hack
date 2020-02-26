from django.db import models
from django.contrib.auth.models import User

# User profile model


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

# Vendor model


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    balance = models.IntegerField()
