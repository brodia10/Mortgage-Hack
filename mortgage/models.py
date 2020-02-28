from django.db import models
from django.contrib.auth.models import User
from mortgage.model_lists import *
from django.dispatch import receiver
from django.db.models.signals import post_save

class Organization(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    balance = models.IntegerField()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,blank=True,null=True)
    last_name = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField(max_length=100,blank=True,null=True)

    organization = models.CharField(verbose_name="Name (ie brand,username)",max_length=100, blank=False,)
    location_city = models.CharField(verbose_name="City",max_length=100, blank=True,)
    location_state = models.CharField(verbose_name="State",choices=state_validation_choices,max_length=2, blank=True,)
    user_type = models.TextField(verbose_name="Which of the following best describes you:",choices=user_type_choices,blank=False,default="",)

    terms_agree = models.TextField(blank=True,default="",verbose_name="I agree to the website's Privacy Policy & Terms and Conditions.")
    # main_picture = models.ImageField(verbose_name="Profile Picture",upload_to = 'media/',blank=True,)
    description = models.TextField(verbose_name="Description",max_length=1500,default="",blank=True)
    parent_organization = models.ForeignKey(Organization,default=None,on_delete=models.CASCADE,blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    balance = models.IntegerField()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
