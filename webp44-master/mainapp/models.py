from django.contrib.auth.models import User
from django.db import models


# A Profile consists of the date of birth, profile image
# that a Member might or might not have, hence the
# OneToOne relationship in Member with null=True
class Profile(models.Model):
    image = models.ImageField(upload_to="profile_images")
    dob = models.DateField(auto_now=False, auto_now_add=False)

    # True if this profile belongs to a Member
    @property
    def has_member(self):
        return hasattr(self, 'member') and self.member is not None

    # Either the username of the Member, or NONE
    @property
    def member_check(self):
        return str(self.member) if self.has_member else 'NONE'

    def __str__(self):
        return self.dob + ' (' + self.member_check + ')'

# Django's User model already has username, password, email
# both of which are required fields, so Member inherits
# these fields
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

    # two properties that count people you like and people who liked you
    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def liked_count(self):
        return Member.objects.filter(likes__id=self.id).count()

    def __str__(self):
        return self.username


# The Message models provides an intermediate model for
# the 'message' ManyToMany relationship between Members
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

    # True if this Hobby belongs to a Member
    @property
    def has_member(self):
        return hasattr(self, 'member') and self.member is not None

    # Either the username of the Member, or NONE
    @property
    def member_check(self):
        return str(self.member) if self.has_member else 'NONE'

    def __str__(self):
        return self.name + ' (' + self.member_check + ')'
