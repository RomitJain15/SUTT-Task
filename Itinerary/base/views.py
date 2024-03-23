from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Group, Trip, Student, Plan, Event, Holiday, Expenditure
from django.contrib.auth.decorators import login_required
from .extract_dates import holiday_dict
import datetime
import requests
from django.db.models import Q
from serpapi import GoogleSearch
import json
# Create your views here.

destinations = ["Mumbai", "Bengaluru", "Jaipur", "Goa", "Kolkata", "Hyderabad", "Chennai", "Ahmedabad"]


def home(request):
    upcoming_events = []
    current_day_events = []
    total_amount_for_trip = {}
    user_trips = []
    user_has_plans = []
    if request.user.is_authenticated:
        student = Student.objects.get(username=request.user.username)
        student.id_number = request.user.email[1:9]
        student.save()
                    
        trips = Trip.objects.all()
        for trip in trips:
            if datetime.date.today() > trip.end_date:
                trip.is_complete = True
                trip.save()
            if trip.is_complete == False:
                if trip.group.members :
                    members_list = trip.group.members.split(',')
                    formatted_members = [member[:4] + member[8:12] for member in members_list if member]
                    if request.user == trip.group.leader or student.id_number in formatted_members:
                        user_trips.append(trip)
                        total_amount_for_trip[trip] = student.total_expenditure_in_trip(trip)
                        if trip.plan_set.filter(creator=request.user).exists():
                            user_has_plans.append(True)
                        else:
                            user_has_plans.append(False)
                elif trip.group.leader == request.user:
                    user_trips.append(trip)
                    if trip.plan_set.filter(creator=request.user).exists():
                            user_has_plans.append(True)
                    else:
                        user_has_plans.append(False)
        print(total_amount_for_trip)

        events = Event.objects.all()
        for event in events:
            if datetime.date.today() == event.date and datetime.datetime.now().time() > event.end_time:
                event.is_done = True
                event.save()
            if event.trip in user_trips:
                if event.is_done == False:
                    upcoming_events.append(event)
                    if event.date == datetime.date.today():
                        current_day_events.append(event)

    

    context = {
        "upcoming_events": upcoming_events,
        "current_day_events": current_day_events,
        "total_amount_for_trip": total_amount_for_trip,
        "trips": user_trips,
        "user_has_plans": user_has_plans,
    }
    return render(request, 'base/home.html', context)

@login_required(login_url="http://127.0.0.1:8000/accounts/google/login/?next=/")
def pastTrips(request):
    total_amount_for_trip = {}
    student = Student.objects.get(username=request.user.username)
    trips = Trip.objects.all()
    for trip in trips:
        if trip.is_complete:
            if trip.group.members :
                members_list = trip.group.members.split(',')
                formatted_members = [member[:4] + member[8:12] for member in members_list if member]
                if request.user == trip.group.leader or student.id_number in formatted_members:
                    total_amount_for_trip[trip] = student.total_expenditure_in_trip(trip)
            elif trip.group.leader == request.user:
                total_amount_for_trip[trip] = student.total_expenditure_in_trip(trip)
    context = {
        "total_amount_for_trip": total_amount_for_trip
    }
    return render(request, 'base/past_trips.html', context)

def pastTripPlans(request, pk):
    plans = Plan.objects.filter(trip=pk)
    context = {
        "plans": plans,
    }
    return render(request, 'base/past_trip_plans.html', context)

def logoutPage(request):
    logout(request)
    return redirect('/')

@login_required(login_url="http://127.0.0.1:8000/accounts/google/login/?next=/")
def createTrip(request):
    month_to_number = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }
    for holiday_date, day in holiday_dict.items():
        holiday = Holiday(date=holiday_date, day=day)
        holiday.save()
    holidays = Holiday.objects.all()
    holidays_list = []
    for holiday in holidays:
        if holiday.day == "M" or holiday.day == "F" or holiday.day == "S" or holiday.day == "Vacation":
            holidays_list.append(holiday.date)
    today = datetime.date.today()
    formatted_date = today.strftime("%B %d %Y").lstrip("0").replace(",", "")
    final_holidays = []
    for holiday_date in holidays_list:
        if holiday_date[-1] >= formatted_date[-1]:
            if month_to_number[holiday_date.split()[0]] == month_to_number[formatted_date.split()[0]]:
                if int(holiday_date.split()[1]) >= int(formatted_date.split()[1]):
                    final_holidays.append(holiday_date)
            elif month_to_number[holiday_date.split()[0]] >= month_to_number[formatted_date.split()[0]]:

                final_holidays.append(holiday_date)

    context = {
        "destinations": destinations,
        "holidays": final_holidays
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


def addPlan(request, pk):
    trip = Trip.objects.get(id=pk)
    if request.method == 'POST':
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
                date=date,
                trip=trip
            )
            plan.events.add(event)
        plan.save()
        return redirect('/')
    print(trip.start_date, trip.end_date)
    context = {
        "start_date": trip.start_date,
        "end_date": trip.end_date
    }
    return render(request, 'base/add_plan.html', context)

def editPlan(request, pk, pk2):
    plan = Plan.objects.get(trip_id=pk, creator__username=pk2)
    events = plan.events.all()
    context = {
        "events": events,
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
    trip = Trip.objects.get(id=trip_id)
    context = {
        "event": event,
        "start_date": trip.start_date,
        "end_date": trip.end_date
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
    if Plan.objects.filter(trip=trip, being_followed=True).exists():
        context = {
            "plans": "Plan already selected"
        }
        return render(request, 'base/select_plan.html', context)
    else:
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

@login_required(login_url="http://127.0.0.1:8000/accounts/google/login/?next=/")
def searchFlights(request):
    API_KEY = "3a2edea6ab85bc60297279ce08d2ab75a71365e5f7e66ca2b3d524b6d326d906"
    best_flights = []
    if request.method == "POST":
        destination = request.POST.get('destination')
        departure_date = request.POST.get('departure_date')
        adult_count = request.POST.get('adults')
        children_count = request.POST.get('children')
        destination_code = {
            "Mumbai": "BOM",
            "Bengaluru": "BLR",
            "Jaipur": "JAI",
            "Goa": "GOI",
            "Kolkata": "CCU",
            "Hyderabad": "HYD",
            "Chennai": "MAA",
            "Ahmedabad": "AMD"
        }
        print(destination_code[destination], departure_date, adult_count, children_count)
        params = {
            "engine": "google_flights",
            "type": 2,
            "departure_id": "DEL",
            "arrival_id": destination_code[destination],
            "outbound_date": departure_date,
            "currency": "INR",
            "hl": "en",
            "api_key": API_KEY,
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        if 'best_flights' in results:
            flights = results['best_flights']
            print(flights)
        else:
            flights = results['other_flights']
            print(flights)
    context = {
        "destinations": destinations,
        "flights": flights
    }
    return render(request, 'base/search_flights.html', context)

def splitCost(request, pk):
    trip = Trip.objects.get(id=pk)
    plan = Plan.objects.filter(trip=trip, being_followed=True).first()
    if plan:
        events = plan.events.all()
        events = events.filter(is_done=True, cost_split=False)
    else:
        events = ""
    context = {
        "plan": plan,
        "events": events,
    }
    return render(request, 'base/split_cost.html', context)

def eventSplitCost(request, pk):
    event = Event.objects.filter(id=pk).first()
    trip = event.trip
    group = trip.group
    group_leader = group.leader
    group_members = group.members.split(',')[0:-1]
    all_members = []
    all_members.append(group_leader)
    for member in group_members:
        all_members.append(Student.objects.filter(id_number=member[:4]+member[8:12]).first())
    if request.method == 'POST':
        amounts = request.POST.getlist('amount[]')
        for i, member in enumerate(all_members):
            amount = amounts[i]
            if amount:
                Expenditure.objects.create(amount=amount, payer=member, event=event)
        event.cost_split = True
        event.save()
        return redirect('home')
    context = {
        "event": event,
        "members": all_members,
    }
    return render(request, 'base/event_split_cost.html', context)