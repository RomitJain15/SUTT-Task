from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout

# Create your views here.

def home(request):
    return render(request, 'base/home.html')

def logoutPage(request):
    logout(request)
    return redirect('/')

def createTrip(request):
    return HttpResponse('Create a Trip')