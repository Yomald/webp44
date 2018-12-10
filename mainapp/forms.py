from django import forms
from django.contrib.admin import widgets

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
    username = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'placeholder': "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email address'}))
    dob = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'Date of birth'}))
    # GENDER_CHOICES = (
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    # )
    # gender = forms.ChoiceField(widgets=forms.Select(ch))
