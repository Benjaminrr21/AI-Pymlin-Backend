from operator import index
from django.urls import path


from . import views

#ovo definise sta ubacujemo u link nakon game/
urlpatterns = [
   #path("",views.index,name="index"),
    path("movee/",views.make_move),
]