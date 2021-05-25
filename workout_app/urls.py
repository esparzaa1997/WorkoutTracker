
from django.urls import path

from .import views

urlpatterns = [
    #Login Page
    path('', views.index),
    #Login POST Form
    path('login', views.login),
    #Register Page
    path('registerpage',views.registerpage),
    #Register POST Form
    path('register', views.register),
    #Home Page
    path('homepage', views.homepage),
    #Logout
    path('logout', views.logout),
    #createworkoutpage
    path('createworkout', views.createworkout),
    #Create Workout
    path('newworkout', views.newworkout),
    #View Workout Page
    path('viewworkout', views.viewworkout),
]
