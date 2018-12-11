from django import forms
from django.contrib.admin import widgets
from mainapp.models import Member, Profile, Hobby, Gender
import datetime as D

# class NameForm(forms.Form):
#     your_name = forms.CharField(label='Your name', max_length=100)
#     username = forms.CharField(label="Username", max_length = 20)
#
# class ContactForm(forms.Form):
#     subject = forms.CharField(max_length=100)
#     message = forms.CharField(widget=forms.Textarea)
#     sender = forms.EmailField()
#     cc_myself = forms.BooleanField(required=False)

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'placeholder': "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))



class RegisterForm(forms.Form):
    genders=Gender.objects.all()
    GENDARR = []
    for x in genders:
        GENDARR.append((x.pk,x.name))

    hobo=Hobby.objects.all()
    HOBBARR = []
    for x in hobo:
        HOBBARR.append((x.pk,x.name))

    now = D.datetime.utcnow()
    age18 =D.timedelta(seconds=365 * 24 * 60 * 60 * 17)
    delta = now - age18
    format = "%Y"
    minage = D.datetime.strftime(delta, format)

    username = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'placeholder': "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email address'}))
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1910,int(minage)),attrs={'class': 'Date of birth'}))
    file = forms.ImageField(widget=forms.FileInput(attrs={'class': 'ProfilePic'}))
    gender = forms.ChoiceField(required=False,choices=GENDARR,widget=forms.Select(attrs={'class': 'Gender'}))
    hobbies = forms.MultipleChoiceField(required=False,choices=HOBBARR,widget=forms.CheckboxSelectMultiple(attrs={'class': 'WHO IS DAT POKÉMON'}))
    # GENDER_CHOICES = (
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    # )
    # gender = forms.ChoiceField(widgets=forms.Select(ch))
