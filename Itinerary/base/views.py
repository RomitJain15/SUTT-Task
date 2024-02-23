from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'base/home.html')

def loginPage(request):
    return HttpResponse('Login Page')

def logoutPage(request):
    return HttpResponse('Logout Page')

def createTrip(request):
    return HttpResponse('Create a Trip')