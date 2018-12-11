from django.urls import path
from mainapp import views

urlpatterns = [
  path('', views.index, name='index'),


  # signup page
  path('createAccount/', views.signup, name='createAccount'),


    # login page
    path('login', views.login, name='login'),

    #member's profile page
    path('member/', views.membersProfile, name='member'),

    #profile page
    path('profile/', views.userProfile, name='profile'),

    path('matches/', views.matches, name='matches'),

    #log out page
    path('logOut/', views.logout, name='logOut'),

    path('getHobbies/', views.getHobbies, name='getHobbies'),


    path('test/', views.test, name='test'),



]
