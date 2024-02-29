from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Student(AbstractUser):
    id_number = models.CharField(max_length=20)
    is_group_leader = models.BooleanField(default=False)
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username
    
class Group(models.Model):
    leader = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='group_leader')
    members = models.ManyToManyField(Student, related_name='group_members')

class Location(models.Model):
    name = models.CharField(max_length=100)
    airport_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Trip(models.Model):
    trip_name = models.CharField(max_length=100)
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='trip_destination')
    start_date = models.DateField()
    end_date = models.DateField()
    group_leader = models.ForeignKey(Student, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='trip_location')

    def __str__(self):
        return self.trip_name

class Plan(models.Model):
    name = models.CharField(max_length=100)
    events = models.ManyToManyField('Event')
    creator = models.ForeignKey(Student, on_delete=models.CASCADE)
    being_followed = models.BooleanField(default=False)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Event(models.Model):
    location = models.CharField(max_length=100)
    activities = models.TextField()
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()

    def __str__(self):
        return f"{self.location} - {self.date}"

class Expenditure(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payer = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Expenditure: {self.amount}, Payer: {self.payer.username}"