from django.db import models
import re
import bcrypt 
# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['password']) < 8:
            errors['password'] = 'password must be at least 8 characters'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address"
        if len(postData['username']) < 2:
            errors['username'] = "Username is too short"
        if postData['password'] != postData['confirmpassword']:
            errors['password'] = "password does not match"
        return errors
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['email'])
        if user:
            log_user = user[0]
            if not bcrypt.checkpw(postData['password'].encode(), log_user.password.encode()):
                errors['password'] = "Invalid Login Attempt"
        else:
            errors['password'] = "Invalid login attempt"
        return errors

class WorkoutManager(models.Manager):
    def workout_validator(self, postData):
        errors = {}
        if len(postData['name']) < 4:
            errors['name'] = 'workout name must be more than 4 characters long'
        
        if len(postData['description']) < 4:
            errors['description'] = "Description is too short"
        return errors

class ExerciseManager(models.Manager):
    def exercise_validator(self, postData):
        errors = {}
        EXERCISE_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['name']) < 4:
            errors['name'] = 'exercise name must be more than 4 characters long'
        if not EXERCISE_REGEX.match(postData['name']):
            errors['name'] = "Exercise name must contain letters, numbers and basic characters only."
        if len(postData['weight']) < 1:
            errors['weight'] = "Need to input an appropiate weight"
        if len(postData['sets']) < 1:
            errors['sets'] = "Need to have something in sets"
        if len(postData['reps']) < 1:
            errors['reps'] = "Need to have something in repeitions"
        return errors

class User(models.Model):
    username = models.CharField(max_length = 45)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 45)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


class Workout(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    user = models.ForeignKey(User, related_name ="workout", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WorkoutManager()

class Exercise(models.Model):
    name = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=999, decimal_places=1)
    sets = models.IntegerField()
    reps = models.DecimalField(max_digits=999, decimal_places=1)
    workout = models.ForeignKey(Workout, related_name ="exercise", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ExerciseManager()