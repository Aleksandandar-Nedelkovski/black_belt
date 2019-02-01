from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django import forms


def index(request):
    if 'id' in request.session:
        return redirect('/dashboard')
    else:
        return render(request, "login/index.html")


def register(request):
    if request.method == "POST":
        check = User.objects.register(
            request.POST['first_name'],
            request.POST['last_name'],
            request.POST['email'],
            request.POST['password'],
            request.POST['confirm']
        )
    if not check['valid']:
        for error in check['errors']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')
    else:
        request.session['id'] = check['id']
        return redirect('/dashboard')


def login(request):
    if request.method == "POST":
        check = User.objects.login(
            request.POST['email'],
            request.POST['password'],
        )
        if not check["valid"]:
            for error in check['errors']:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/')
        else:
            request.session['id'] = check['id']
            return redirect('/dashboard')


def logout(request):
    if 'id' in request.session:
        request.session.clear()
        messages.add_message(request, messages.SUCCESS, "Thank you for using Handy Helper. See you later")
        return redirect('/')
    else:
        return render(request, "login/index.html")

def dashboard(request):
    user = User.objects.get(id=request.session['id'])
    all_jobs = Job.objects.filter(fav_job=None)
    fav_jobs =  user.favorites.all()
    context={
        'fav_jobs': fav_jobs,
        'all_jobs': all_jobs,
        'user': user,
    }
    return render(request, "login/dashboard.html", context)

def add_job(request):
    if 'id' in request.session:
        return render(request, 'login/addjob.html')
    else:
        return redirect('/dashboard')


def addjob(request):
    if request.method == "POST":
        errors = Job.objects.job_validator(request.POST)
        if len(request.POST['title']) < 3:
            messages.error(request, "Title must be longer than 3 characters.")
        if len(request.POST['desc']) < 10:
            messages.error(request, "Description must be more than 10 characters.")
        if len(request.POST['location']) < 1:
            messages.error(request, "Location can't be blank.")
            return redirect('/add_job')
        else:
            user = User.objects.get(id=request.session['id'])
            Job.objects.create(uploaded_by=user, title=request.POST['title'], desc=request.POST['desc'], location=request.POST['location'])
            return redirect('/dashboard')


def add_favorite(request, id):
    user = User.objects.get(id=request.session['id'])
    job = Job.objects.get(id= id)
    job.fav_job = user
    job.save()
    print(job.fav_job.first_name)
    return redirect('/dashboard')


def view(request, id):
    all_jobs = Job.objects.filter(id=id)
    context={
        'all_jobs': all_jobs,
    }
    return render(request, "login/view.html", context)


def edit(request, id):
    all_jobs = Job.objects.get(id=id)
    context={
        'all_jobs': all_jobs,
    }
    return render(request, "login/edit.html", context)


def update_jobs(request, id):
    if request.method == "POST":
        errors = Job.objects.job_validator(request.POST)
        if len(request.POST['title']) < 3:
            messages.error(request, "Title must be longer than 3 characters.")
        if len(request.POST['desc']) < 10:
            messages.error(request, "Description must be more than 10 characters.")
        if len(request.POST['location']) < 1:
            messages.error(request, "Location can't be blank.")
            return redirect('/edit/'+id)
        else:
            c = Job.objects.get(id=id)
            c.title = request.POST['title']
            c.desc = request.POST['desc']
            c.location = request.POST['location']
            c.save()
            return redirect('/dashboard')

def delete_fav(request, id):
    job = Job.objects.get(id = id)
    job.delete()
    return redirect('/dashboard')