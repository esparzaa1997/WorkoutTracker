from django.shortcuts import render, HttpResponse, redirect
from .models import User,Workout,Exercise
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, "login.html")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['logged_in_user'] = user.id
    return redirect('/homepage')

def registerpage(request):
    return render(request, "register.html")

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/registerpage")
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        newuser = User.objects.create(username = request.POST['username'], email = request.POST['email'], password = hash1)
        request.session['logged_in_user'] = newuser.id
        return redirect('/homepage')

def logout(request):
    del request.session['logged_in_user']
    return redirect('/')

def homepage(request):
    if 'logged_in_user' not in request.session:
        return redirect('/')
    else:
        context = {
                'logged_in': User.objects.get(id=request.session['logged_in_user']),
            }
        return render(request, 'homepage.html', context)

def createworkout(request):
    if 'logged_in_user' not in request.session:
        return redirect('/')
    else:
        context = {
                'logged_in': User.objects.get(id=request.session['logged_in_user']),
            }
        return render(request, 'createworkout.html', context)

def newworkout(request):
    if 'logged_in_user' not in request.session:
        return redirect('/')
    else:
        errors = Workout.objects.workout_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/createworkout")
        else:
            user = User.objects.get(id = request.session['logged_in_user'])
            Workout.objects.create(name = request.POST['name'], description = request.POST['description'], user = user)
            return redirect('/viewworkout')

def viewworkout(request):
    if 'logged_in_user' not in request.session:
        return redirect('/')
    else:
        
        return render(request, 'viewworkout.html')