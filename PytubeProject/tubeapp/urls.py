from django.urls import path
from tubeapp.views import index, search, prepare, download

urlpatterns = [
    path('', index, name='tubeapp'),
    path('search', search),
    path('prepare', prepare),
    path('download/<str:name>', download)
]
