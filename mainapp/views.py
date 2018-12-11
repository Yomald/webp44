from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, Http404, JsonResponse, QueryDict, HttpResponseRedirect
from django.template import RequestContext, loader
from mainapp.models import Member, Profile, Hobby, Gender
from django.contrib.auth.hashers import make_password
from django.core import serializers
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import json
from .forms import LoginForm, RegisterForm
from django.core.mail import send_mail
import datetime as D

appname = 'MatchMe'

def index(request):
    context = { 'appname': appname }
    return render(request,'mainapp/index.html',context)


def loggedin(view):
    def mod_view(request):
        if 'username' in request.session:
            username = request.session['username']
            try: user = Member.objects.get(username=username)
            except Member.DoesNotExist: raise Http404('Member does not exist')
            return view(request, user)
        else:
            return render(request,'mainapp/not-logged-in.html',{})
    return mod_view

# Create your views here.
def login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try: member = Member.objects.get(username=username)
            except Member.DoesNotExist: raise ValidationError(('Username DoesNotExist'), code='DoesNotExist')
            if member.check_password(password):
                # remember user in session variable
                request.session['username'] = username
                request.session['password'] = password
                context = {
                   'appname': appname,
                   'username': username,
                   'profile': member.profile,
                   'loggedin': True
                }
                response = render(request, 'mainapp/matches.html', context)

                # remember last login in cookie
                now = D.datetime.utcnow()
                max_age = 365 * 24 * 60 * 60  #one year
                delta = now + D.timedelta(seconds=max_age)
                format = "%a, %d-%b-%Y %H:%M:%S GMT"
                expires = D.datetime.strftime(delta, format)
                response.set_cookie('last_login',now,expires=expires)

                return response
    else:
        form = LoginForm()

    return render(request, 'mainapp/login.html', {'form': form})

def signup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            em = form.cleaned_data['email']
            hobs = form.cleaned_data['hobbies']
            helicopter = form.cleaned_data['gender']
            dateob = form.cleaned_data['dob']
            image_file = form.cleaned_data['file']
            hobbiesar = []
            for x in hobs:
                hobby = Hobby.objects.get(pk = x)
                hobbiesar.append(hobby)
            gend = Gender.objects.get(pk = helicopter)
            prof = Profile(image = image_file, dob=dateob)
            prof.save()
            user = Member(username = u,
                         email = em,
                          profile = prof,
                          gender =gend
                          )
            user.set_password(p)
            user.save()
            user.hobbies.set(hobbiesar)
            return HttpResponseRedirect('/login')
    else:
        form = RegisterForm()

    return render(request, 'mainapp/createAccount.html', {'form': form})

    # context = { 'appname': appname }

def membersProfile(request):
    context = { 'appname': appname }
    return render(request,'mainapp/member.html',context)

@loggedin
def editprofile(request, user):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            em = form.cleaned_data['email']
            hobs = form.cleaned_data['hobbies']
            helicopter = form.cleaned_data['gender']
            dateob = form.cleaned_data['dob']
            image_file = form.cleaned_data['file']
            hobbiesar = []
            for x in hobs:
                hobby = Hobby.objects.get(pk = x)
                hobbiesar.append(hobby)
            gend = Gender.objects.get(pk = helicopter)
            #prof = Profile(image = image_file, dob=dateob)
            user.profile.image.set(image_file)
            user.profile.dob.set(dateob)
            user.username.set(username)
            user.email.set(email)
            user.gender.set(gender)
            user.set_password(p)
            user.hobbies.set(hobbiesar)
            return HttpResponseRedirect('/editprofile')
    else:
        form = RegisterForm()

    return render(request, 'mainapp/createAccount.html', {'form': form})

@loggedin
def getProfile(request, user):
    if request.method == "GET":
        json_res = dict(
            username = user.username,
            email = user.email,
            hobbies = user.hobbies.all(),
            gender = user.gender,
            image = user.profile.image
        )
        return JsonResponse(json_res, safe=False)
    else:
        raise Http404("Not a GET Method")

@loggedin
def matches(request, user):
    context = {
        'appname': appname,
        'username': user.username,
        'profile' : user.profile,
        'loggedin': True
    }
    return render(request,'mainapp/matches.html',context)

@loggedin
def userProfile(request,user):
    context = {
        'appname': appname,
        'username': user.username,
        'profile' : user.profile,
        'loggedin': True
    }
    return render(request,'mainapp/profile.html',context)

def logout(request):
    context = { 'appname': appname }
    return render(request,'mainapp/logOut.html',context)

def test(request):
    context = { 'appname': appname }
    return render(request,'mainapp/test.html',context)


@loggedin
def getUsersWithSameHobbies(request, user):
    userhobarr = []
    for x in user.hobbies.all():
        userhobarr.append(x.name)
    json_res = []
    for x in Member.objects.all():
        if x != user or x == user:
            memberhobarr = []
            for y in x.hobbies.all():
                memberhobarr.append(y.name)
            asd = []
            for z in set(userhobarr).intersection(memberhobarr):
                asd.append(z)
            json_obj = dict(
                id = x.id,
                name = x.username,
                commonhno = len(set(userhobarr).intersection(memberhobarr)),
                commonh = asd,
                gender = x.gender.name,
                dob = str(x.profile.dob)
            )
            json_res.append(json_obj)
        # ut.sort(key=lambda x: x.count, reverse=True)
    json_res.sort(key=lambda x: x['commonhno'], reverse=True)
    print(json_res)
    return JsonResponse(json_res, safe=False)

@loggedin
def likeUser(request, user):
    likeID = request.POST['likeID']
    user.likes.add(likeID)

def getHobbies(request):
    allhobbies = serializers.serialize('json',Hobby.objects.all())
    return JsonResponse(allhobbies, safe=False)
