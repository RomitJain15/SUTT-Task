from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('logout/', views.logoutPage, name="logout"),
    path('create-trip', views.createTrip, name="create-trip"),
    path('search-flights', views.searchFlights, name="search-flights"),
    path('add-plan/<int:pk>', views.addPlan, name="add-plan"),
    path('edit-plan/<int:pk>', views.editPlan, name="edit-plan"),
]