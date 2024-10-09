from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import *
from .forms import *
import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse
from datetime import datetime, time

def index(request):
    return render(request, "pages/index.html")

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = Account(email=email, password=password)
            user.save()
            #hash password


            form.save()
            messages.success(request, f'Your account has been created. You can log in now!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'pages/register.html', context)



def home(request):
    return render(request, "pages/home.html")

def portfolio(request):
    return render(request, "pages/portfolio.html")

def watchlist(request):
    return render(request, "pages/watchlist.html")

def notifications(request):
    return render(request, "pages/notifications.html")

from django.shortcuts import render

def stock_search(request):
    query = request.GET.get('query', '')  # Capture the query parameter from the URL
    # Do something with the query, like searching a database
    context = {'query': query}
    return render(request, 'pages/stock_search.html', context)


def watchlist(request):
    return render(request, "pages/watchlist.html")

def notifications(request):
    return render(request, "pages/notifications.html")

def portfolio(request):
    return render(request, "pages/portfolio.html")

def watchlist(request):
    return render(request, "pages/watchlist.html")

def notifications(request):
    return render(request, "pages/notifications.html")

from django.shortcuts import render

def stock_search(request):
    query = request.GET.get('query', '')  # Capture the query parameter from the URL
    # Do something with the query, like searching a database
    context = {'query': query}
    return render(request, 'pages/stock_search.html', context)
