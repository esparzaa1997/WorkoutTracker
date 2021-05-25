
from django.urls import path, include

urlpatterns = [
    path('', include('workout_app.urls')),
]
