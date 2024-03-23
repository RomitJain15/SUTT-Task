from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Student(AbstractUser):
    id_number = models.CharField(max_length=20)
    is_group_leader = models.BooleanField(default=False)

    def total_expenditure_in_trip(self, trip):
        return Expenditure.objects.filter(payer=self, event__trip=trip).aggregate(total_amount=models.Sum('amount'))['total_amount'] or 0

    def __str__(self):
        return self.username
    
class Group(models.Model):
    leader = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='group_leader')
    members = models.CharField(max_length=255, null=True, blank=True)

    
class Trip(models.Model):
    trip_name = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.trip_name

class Plan(models.Model):
    events = models.ManyToManyField('Event')
    creator = models.ForeignKey(Student, on_delete=models.CASCADE)
    being_followed = models.BooleanField(default=False)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class Event(models.Model):
    location = models.CharField(max_length=100)
    activities = models.TextField()
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    is_done = models.BooleanField(default=False)
    trip  = models.ForeignKey(Trip, on_delete=models.CASCADE, blank=True, null=True)
    cost_split = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.location} - {self.date}"
    
    class Meta:
        ordering = ['date', 'start_time']


class Expenditure(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payer = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Expenditure: {self.amount}, Payer: {self.payer.username}"
    
class Holiday(models.Model):
    date = models.CharField(max_length=100, primary_key=True)
    day = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.date} - {self.day}"
