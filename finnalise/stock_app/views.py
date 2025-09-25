from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Stock
# Create your views here.
@login_required
def dashboard(request):
    user_stocks = Stock.objects.filter(user= request.user)
    return render(request , "stock_app/dashboard.html")


def index(request):
    return render(request, "stock_app/index.html")

def room(request,room_name):
    return render(request, "stock_app/room.html",{"room_name": room_name})