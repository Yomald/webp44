from django.shortcuts import render
from django.http import HttpResponse, Http404

appname = 'DatingApp'

# Create your views here.
def index(request):
    # return HttpResponse("HOT MEMES!")
    context = { 'appname': appname }
    return render(request,'mainapp/index.html',context)
