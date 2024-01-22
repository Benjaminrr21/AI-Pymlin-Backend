from operator import index
from django.urls import path
from .views import my_json_view

from . import views

#ovo definise sta ubacujemo u link nakon game/
urlpatterns = [
    path("",views.index,name="index"),
    path("myjson/",my_json_view,name="myjson"),
]