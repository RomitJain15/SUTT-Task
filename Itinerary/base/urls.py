from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('logout/', views.logoutPage, name="logout"),
    path('create-trip', views.createTrip, name="create-trip"),
    path('delete-trip/<int:pk>', views.deleteTrip, name="delete-trip"),
    path('search-flights', views.searchFlights, name="search-flights"),
    path('add-plan/<int:pk>', views.addPlan, name="add-plan"),
    path('edit-plan/<int:pk>/<str:pk2>', views.editPlan, name="edit-plan"),
    path('delete-plan/<int:pk>', views.deletePlan, name="delete-plan"),
    path('edit-event/<int:pk>', views.editEvent, name="edit-event"),
    path('delete-event/<int:pk>', views.deleteEvent, name="delete-event"),
    path('select-plan/<int:pk>', views.selectPlan, name="select-plan"),
    path('split-cost/<int:pk>', views.splitCost, name="split-cost"),
    path('event-split-cost/<int:pk>', views.eventSplitCost, name="event-split-cost"),
    path('past-trips', views.pastTrips, name="past-trips"),
    path('past-trip-plans/<int:pk>', views.pastTripPlans, name="past-trip-plans"),
]