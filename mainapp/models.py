from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    image = models.ImageField(upload_to="profile_images")
    dob = models.DateField(auto_now=False, auto_now_add=False)


class Member(User):
    profile = models.OneToOneField(
        to=Profile,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    hobbies = models.ManyToManyField(
        to='Hobby',
        blank=True,
        symmetrical=False,
        related_name='related_to'
    )
    likes = models.ManyToManyField(
        to='self'   ,
        blank=True,
        symmetrical=True
    )
    #FFFFFFFFFFFFUUUUUUUUUUUUUUUCCCCCCCCCCCCCKKKKKKKKKKKKKDDDDDDDDDIIIIIIIIIISSSSSSSSSSSSSS

class Hobby(models.Model):
    name = models.CharField(max_length=254)
    desc = models.CharField(max_length=254)
