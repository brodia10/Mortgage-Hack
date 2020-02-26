from django.db import models
from django.contrib.auth.models import User

#User profile model
class Profile(models.Model):
    user = models.ForeignKey(User)
    first_name = models.CharField(max_length=255)
    last_name = models.IntegerField()
    email = models.CharField(max_length=255)

#Vendor model
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    balance = models.IntegerField()


