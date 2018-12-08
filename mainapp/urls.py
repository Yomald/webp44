from django.urls import path
from mainapp import views

urlpatterns = [
  path('', views.index, name='index'),

  # signup page
  path('createAccount/', views.signup, name='createAccount'),

  path('register/', views.register, name='register'),

  # index page
  path('index/', views.index, name='index'),

    # home/friends page
    path('friends/', views.login, name='friends'),

    #member's profile page
    path('member/', views.membersProfile, name='member'),

    #profile page
    path('profile/', views.userProfile, name='profile'),

    #log out page
    path('logOut/', views.logout, name='logOut'),

    path('getHobbies/', views.getHobbies, name='getHobbies'),


    path('test/', views.test, name='test'),



]
