from django.urls import path
from tubeapp.views import *

urlpatterns = [
    path('', index),
    path('/search', search),
    path('/download', download),
]
