from django import forms
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def home(request):
    return render_to_response("index.html")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/index/")
    else:
        form = UserCreationForm()
    return render_to_response("register.html", {
        'form': form,
    })

def contact(request):
    return render_to_response("contact.html")

def inquire(request):
    disk={}    
    if request.POST:
        disk["table"]=[x for x in range(20)]
    return render_to_response("inquire.html",disk)
    
def appointment(request):
    return render_to_response("appointment.html")
