from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# forms

# Create your views here.
from django.shortcuts import render, HttpResponse


@login_required(login_url="login")
def home(request):
    return render(request, "home.html")
