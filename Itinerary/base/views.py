from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.db.models import Q
from .models import Group, Trip, Student, Plan, Event
from django.contrib.auth.decorators import login_required
from .forms import EventForm

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
                formatted_members = [member[:4] + member[8:12] for member in members_list if member]
                if request.user == trip.group.leader or student.id_number in formatted_members:
                    user_trips.append(trip)
    context = {
        "upcoming_events": upcoming_events,
        "current_day_events": current_day_events,
        "total_amount": total_amount,
        "trips": user_trips,
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

def deleteTrip(request, pk):
    trip = Trip.objects.get(id=pk)
    context = {
        "obj": trip
    }
    if request.method == "POST":
        trip.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)

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

def editPlan(request, pk, pk2):
    plan = Plan.objects.get(trip_id=pk, creator__username=pk2)
    events = plan.events.all()
    context = {
        "events": events
    }

    if request.method == "POST":
        event_count = request.POST.get('event_count', 0)
        for i in range(1, int(event_count) + 1):
            location = request.POST.get(f'location_{i}')
            activities = request.POST.get(f'activities_{i}')
            estimated_cost = request.POST.get(f'cost_{i}')
            start_time = request.POST.get(f'start_time_{i}')
            end_time = request.POST.get(f'end_time_{i}')
            date = request.POST.get(f'date_{i}')

            # Create a new Event object and associate it with the Plan
            event = Event.objects.create(
                location=location,
                activities=activities,
                estimated_cost=estimated_cost,
                start_time=start_time,
                end_time=end_time,
                date=date
            )
            plan.events.add(event)
        plan.save()

    return render(request, 'base/edit_plan.html', context)

def deletePlan(request, pk):
    plan = Plan.objects.get(id=pk)
    context = {
        "obj": plan
    }
    if request.method == "POST":
        events = plan.events.all()
        events.delete()
        plan.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)

def editEvent(request, pk):
    event = Event.objects.get(id=pk)
    plan = event.plan_set.first()
    trip_id = plan.trip.id
    context = {
        "event": event
    }
    if request.method == "POST":
        event.location = request.POST.get('location')
        event.activities = request.POST.get('activities')
        event.estimated_cost = request.POST.get('cost')
        event.start_time = request.POST.get('start_time')
        event.end_time = request.POST.get('end_time')
        event.date = request.POST.get('date')
        event.save()
        return redirect('edit-plan', pk=trip_id, pk2=request.user.username)
    return render(request, 'base/edit_event.html', context)

def deleteEvent(request, pk):
    event = Event.objects.get(id=pk)
    plan = event.plan_set.first()
    trip_id = plan.trip.id
    context = {
        "obj": event
    }
    if request.method == 'POST':
        event.delete()
        print(plan.events.all() == None)
        if not plan.events.exists():
            plan.delete()
            return redirect('home')
        return redirect('edit-plan', pk=trip_id, pk2=request.user.username)
    return render(request, 'base/delete.html', context)

def selectPlan(request, pk):
    trip = Trip.objects.get(id=pk)
    plans = Plan.objects.filter(trip=trip)
    context = {
        "plans": plans
    }
    
    if request.method == "POST":
        selected_plan_id = request.POST.get('selected_plan')
        selected_plan = Plan.objects.get(id=selected_plan_id)
        selected_plan.being_followed = True
        selected_plan.save()
        return redirect('home')
    return render(request, 'base/select_plan.html', context)