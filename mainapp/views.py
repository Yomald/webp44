from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, Http404, JsonResponse, QueryDict, HttpResponseRedirect
from django.template import RequestContext, loader
from mainapp.models import Member, Profile, Hobby, Gender
from django.contrib.auth.hashers import make_password
from django.core import serializers
from django.db import IntegrityError
import json
from .forms import LoginForm, RegisterForm
from django.core.mail import send_mail

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
def login_page(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')
        # if form.is_valid():
        #     subject = form.cleaned_data['subject']
        #     message = form.cleaned_data['message']
        #     sender = form.cleaned_data['sender']
        #     cc_myself = form.cleaned_data['cc_myself']
        #
        #     recipients = ['info@example.com']
        # if cc_myself:
        #     recipients.append(sender)
        #
        #     send_mail(subject, message, sender, recipients)
        #     return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'mainapp/login.html', {'form': form})
    #
    # context = { 'appname': appname }
    # return render(request,'mainapp/index.html',context)

def signup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')
        # if form.is_valid():
        #     subject = form.cleaned_data['subject']
        #     message = form.cleaned_data['message']
        #     sender = form.cleaned_data['sender']
        #     cc_myself = form.cleaned_data['cc_myself']
        #
        #     recipients = ['info@example.com']
        # if cc_myself:
        #     recipients.append(sender)
        #
        #     send_mail(subject, message, sender, recipients)
        #     return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    return render(request, 'mainapp/createAccount.html', {'form': form})

    # context = { 'appname': appname }

def login(request):
    print(request.POST)
    if 'username' in request.POST:
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

def membersProfile(request):
    context = { 'appname': appname }
    return render(request,'mainapp/member.html',context)

def userProfile(request):
    context = { 'appname': appname }
    return render(request,'mainapp/profile.html',context)

def logout(request):
    context = { 'appname': appname }
    return render(request,'mainapp/logOut.html',context)

def test(request):
    context = { 'appname': appname }
    return render(request,'mainapp/test.html',context)

def register(request):
    if request.POST['username'] == "" or request.POST['password'] == "":
        context = { 'appname': appname }
        return render(request,'mainapp/createAccount.html',context)
    else:
        u = request.POST['username']
        p = request.POST['password']
        if 'img_file' in request.FILES:
            image_file = request.FILES['img_file']
        hobs = request.POST['hobbies']
        hobbiesar = []
        for x in hobs:
            hobby = Hobby.objects.get(pk = x)
            hobbiesar.append(hobby)
        em = request.POST['email']
        helicopter = request.POST['gender']
        dateob = request.POST['dob']
        gend = Gender.objects.get(name = helicopter)
        prof = Profile(image = image_file, dob=dateob)
        prof.save()
        user = Member(username = u,
                        password = p,
                     email = em,
                      profile = prof,
                      gender =gend
                      )
        user.save()
        user.hobbies.set(hobbiesar)
        context = { 'appname': appname }
        render(request,'mainapp/index.html',context)

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

@loggedin
def likeUser(request, user):
    likeID = request.POST['likeID']
    user.likes.add(likeID)

def getHobbies(request):
    allhobbies = serializers.serialize('json',Hobby.objects.all())
    return JsonResponse(allhobbies, safe=False)
