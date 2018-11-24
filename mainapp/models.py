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
    messages = models.ManyToManyField(
        to='self',
        blank=True,
        symmetrical=False,
        through='Message',
        related_name='related_to'
    )
    gender = models.ForeignKey('Gender', on_delete=models.CASCADE)
    #FFFFFFFFFFFFUUUUUUUUUUUUUUUCCCCCCCCCCCCCKKKKKKKKKKKKKDDDDDDDDDIIIIIIIIIISSSSSSSSSSSSSS


class Message(models.Model):
    sender = models.ForeignKey(
        to=Member,
        related_name='sent',
        on_delete=models.CASCADE
    )
    recip = models.ForeignKey(
        to=Member,
        related_name='received',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=4096)
    time = models.DateTimeField()

    def __str__(self):
        return 'From ' + self.sender.username + ' to ' + self.recip.username

class Gender(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Hobby(models.Model):
    name = models.CharField(max_length=254)
    desc = models.CharField(max_length=254)
