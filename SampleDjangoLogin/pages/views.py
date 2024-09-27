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
    return render(request, "pages/stintGraph.html")

def project_list(request):
    project = Project.objects.all()
    return render(request, "pages/project_details.html", {"projects": project})

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

def CUStudent(request, student_id=None):
    studentObj = None
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
           ab = student_form.save()
           ab.save()
           return HttpResponseRedirect('/pages/studentlist/')
    else:
        if request.method == 'GET':
            if student_id:
                studentObj = Project.objects.get(pk=student_id)
                #Only Task creater can make task Public or Private
                student_form = StudentForm(instance=studentObj)
            else:
                student_form = StudentForm()

    return render(request, 'pages/NewStudent.html', {'StudentForm_form': student_form,
                                                              'studentObj': studentObj, })


def newProject(request, product_id=None):
    groupObj = None
    if request.method == 'POST':
        group_form = NewProjectForm(request.POST)
        if group_form.is_valid():
           groupF = group_form.save()
           groupF.save()
           return HttpResponseRedirect('/pages/list/')
    else:
        if request.method == 'GET':
            if product_id:
                groupObj = Project.objects.get(pk=product_id)
                #Only Task creater can make task Public or Private
                group_form = NewProjectForm(instance=groupObj)
            else:
                group_form = NewProjectForm()

    return render(request, 'pages/NewProject.html', {'GroupForm_form': group_form,
                                                              'groupobj': groupObj, })

def project_index(request):
    projects = Project.objects.all()
    context = {
        "projects": projects
    }
    return render(request, "pages/project_index.html", context)

def home(request):
    project = Project.objects.all()
    #return render(request, "pages/project_details.html", {"projects": project})
    return render(request, "pages/home.html", {"projects": project})


def handle_delete_item_request(request, product_id):
    item = Project.objects.get(id=product_id)
    item.delete()
    project = Project.objects.all()
    return render(request, "pages/project_details.html", {"projects": project})

def handle_game_details_request(request, game_id=None):
    game_id = request.GET.get("game_id")
    #print(game_id)
    stats = gameStints.objects.filter(gameID='202306010DEN')
    dataTable = {}
    homeScore = []
    awayScore = []
    homePos = []
    awayPos = []
    stintStart = []
    stintEnd = []
    stints = []

    for row in stats:
        homeScore.append(row.homeScore)
        awayScore.append(row.awayScore)
        homePos.append(row.homePos)
        awayPos.append(row.awayPos)
        stintStart.append(row.stintStart)
        stintEnd.append(row.stintEnd)
        startTime_object = datetime.strptime(row.stintStart, '%H:%M:%S')
        endTime_object = datetime.strptime(row.stintEnd, '%H:%M:%S')#.time()
        diff = startTime_object - endTime_object
        stints.append(diff.total_seconds())
        
    dataTable[0] ={"homeScore": homeScore, "awayScore": awayScore, "homePos": homePos, "awayPos": awayPos, "stintStart":stintStart, "stintEnd":stintEnd, "stints": stints}
    data = json.dumps(dataTable)   
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def profile_view(request):
    if request.user.is_authenticated:
        user_email = request.user.email
        # Use user_email in your view logic
    else:
        user_email = "Not logged in"
    return render(request, 'profile.html', {'user_email': user_email})