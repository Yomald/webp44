from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from mainapp.models import Member, Profile
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
import json


# datetime library to get time for setting cookie
import datetime as D
import sys

appname = 'DatingApp'

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
def index(request):
    # return HttpResponse("HOT MEMES!")
    context = { 'appname': appname }
    return render(request,'mainapp/index.html',context)

def login(request):
    if request.POST['username'] == "" or request.POST['password'] == "":
        context = { 'appname': appname }
        return render(request,'mainapp/login.html',context)
    else:
        username = request.POST['username']
        password = request.POST['password']
        try: member = Member.objects.get(username=username)
        except Member.DoesNotExist: raise Http404('User does not exist')
        if member.check_password(password):
            # remember user in session variable
            request.session['username'] = username
            request.session['password'] = password
            context = {
               'appname': appname,
               'username': username,
               'loggedin': True
            }
            response = render(request, 'mainapp/login.html', context)
            # remember last login in cookie
            now = D.datetime.utcnow()
            max_age = 365 * 24 * 60 * 60  #one year
            delta = now + D.timedelta(seconds=max_age)
            format = "%a, %d-%b-%Y %H:%M:%S GMT"
            expires = D.datetime.strftime(delta, format)
            response.set_cookie('last_login',now,expires=expires)
            return response
        else:
            raise Http404('Wrong password')

def register(request):
    if request.POST['username'] == "" or request.POST['password'] == "":
        context = { 'appname': appname }
        return render(request,'mainapp/register.html',context)
    else:
        u = request.POST['username']
        p = request.POST['password']
        if 'img_file' in request.FILES:
            image_file = request.FILES['img_file']
        hobbies = request.POST['hobbies']
        em = request.POST['email']
        helicopter = request.POST['gender']
        dateob = request.POST['dob']
        # TODO hobbies implementation,
        try:
            user = Member(username = u,
                          password = p,
                          email = em,
                          profile = Profile(image = image_file, dob = dateob),
                          gender = helicopter
                          )
            user.save()
        except:
            raise Http404("WTF ARE U DOING?")
        render(request,'mainapp/login.html',context)

@loggedin
def getUsersWithSameHobbies(request, user):
    json_res = []
    for x in Member:
        json_obj = dict(
            id = x.id,
            name = x.username,
            commonhno = len(set(user.hobbies).intersection(x.hobbies)),
            commonh = set(user.hobbies).intersection(x.hobbies),
            gender = x.gender,
            dob = x.dob
        )
        json_res.append(json_obj)
        # ut.sort(key=lambda x: x.count, reverse=True)
    json_res.sort(key=lambda x: x.commonhno, reverse=True)
    return JsonResponse(json_res, safe=False)
