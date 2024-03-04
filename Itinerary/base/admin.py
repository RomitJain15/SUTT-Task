from django.contrib import admin
from .models import Student, Group, Trip, Plan, Event, Expenditure, Holiday
# Register your models here.
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Trip)
admin.site.register(Plan)
admin.site.register(Event)
admin.site.register(Expenditure)
admin.site.register(Holiday)