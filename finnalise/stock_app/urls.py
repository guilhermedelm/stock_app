from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name = "dashboard"),
    path("",views.index,name = "index"),
    path("<str:room_name>/",views.room,name="room"),
]