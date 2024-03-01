from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from .models import Group, Trip

# Create your views here.

destinations = ["Mumbai", "Bengaluru", "Jaipur", "Goa", "Kolkata", "Hyderabad", "Chennai", "Ahmedabad"]

def home(request):
    upcoming_events = []
    current_day_events = []
    total_amount = 0
    context = {
        "upcoming_events": upcoming_events,
        "current_day_events": current_day_events,
        "total_amount": total_amount 
    }
    return render(request, 'base/home.html', context)

def logoutPage(request):
    logout(request)
    return redirect('/')

def createTrip(request):
    context = {
        "destinations": destinations
    }

    if request.method == 'POST':
        trip_name = request.POST.get('trip-name')
        selected_destination = request.POST.get('destination')
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')

        leader = request.user

        trip = Trip.objects.create(
            trip_name=trip_name,
            destination=selected_destination,
            start_date=start_date,
            end_date=end_date
            )

        group = Group.objects.create(leader=leader)
        member_ids = request.POST.getlist('member-id')
        if len(member_ids) != 0:
            group.members = ""
        for member_id in member_ids:
            group.members += member_id + ","

        group.save()

        trip.group = group
        trip.save()
        return redirect('/')

    return render(request, 'base/create_trip.html', context)