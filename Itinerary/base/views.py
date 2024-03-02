from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.db.models import Q
from .models import Group, Trip, Student, Plan, Event
from django.contrib.auth.decorators import login_required

# Create your views here.

destinations = ["Mumbai", "Bengaluru", "Jaipur", "Goa", "Kolkata", "Hyderabad", "Chennai", "Ahmedabad"]

def home(request):
    upcoming_events = []
    current_day_events = []
    total_amount = 0
    user_trips = []
    if request.user.is_authenticated:
        student = Student.objects.get(username=request.user.username)
        student.id_number = request.user.email[1:9]
        student.save()

        trips = Trip.objects.all()
        for trip in trips:
            if trip.group.members:
                members_list = trip.group.members.split(',')
                formatted_members = [member[:4] + member[-4:] for member in members_list if member]
                if request.user == trip.group.leader or student.id_number in formatted_members:
                    user_trips.append(trip)

    context = {
        "upcoming_events": upcoming_events,
        "current_day_events": current_day_events,
        "total_amount": total_amount,
        "trips": user_trips
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

def searchFlights(request):
    context = {}
    return render(request, 'base/search_flights.html', context)

def addPlan(request, pk):
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk)
        plan = Plan.objects.create(creator=request.user, trip=trip)
        event_count = int(request.POST.get('event_count'))
        for i in range(1, event_count + 1):
            location = request.POST.get(f'location_{i}')
            activities = request.POST.get(f'activities_{i}')
            cost = request.POST.get(f'cost_{i}')
            start_time = request.POST.get(f'start_time_{i}')
            end_time = request.POST.get(f'end_time_{i}')
            date = request.POST.get(f'date_{i}')

            event = Event.objects.create(
                location=location,
                activities=activities,
                estimated_cost=cost,
                start_time=start_time,
                end_time=end_time,
                date=date
            )
            plan.events.add(event)
        plan.save()
        return redirect('/')
    return render(request, 'base/add_plan.html')

def editPlan(request):
    pass