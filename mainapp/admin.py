from django.contrib import admin
from .models import *

class ProfileAdmin(admin.ModelAdmin):
    fields = ('image','dob')
    list_display = ('dob','member_check')
    ordering = ['dob']

class MemberAdmin(admin.ModelAdmin):
    fields = ('username','password','email', 'profile', 'likes', 'gender')
    list_display = ('username','password','likes_count', 'liked_count')
    ordering = ['username']

class MessageAdmin(admin.ModelAdmin):
    fields = ('sender','recip','text','time')
    list_display = ('time','sender','recip','text')
    ordering = ['-time']

class HobbyAdmin(admin.ModelAdmin):
    fields = ('name','desc')
    list_display = ('name', 'member_check')
    ordering = ['name']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Hobby, HobbyAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Gender)
