#from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

def index(request):
    return JsonResponse({'Hello world. You are in a game...':'GGG'})
# Create your views here.

def my_json_view(request):
    data = {'Benjamin': 'Ramovic'}
    return JsonResponse(data)
