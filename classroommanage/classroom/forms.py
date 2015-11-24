# -*- coding: utf-8 -*-
#from django.db import models
from django.forms import ModelForm
from django import forms
from models import Room, Building, Order
from django.contrib.auth.models import User
from classroommanage import globalty

class InqureForm(forms.Form):
    day = forms.DateField(label = u'日期')
    period = forms.ChoiceField(choices = globalty.Period_list, label = u'节次')
    campus = forms.ChoiceField(choices = globalty.Campus_list, label = u'校区')
    building = forms.ChoiceField(choices = globalty.Build_list, label = u'教学楼')
    
class FreeroomForm(ModelForm):
    class Meta:
        model = Room
        exclude = ('user')

class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ('user', 'is_dealed', 'is_agreed')

class InformationForm(ModelForm):
    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'is_superuser', 'last_login', \
        'date_joined', 'password', 'groups', 'user_permissions')

class YourroomForm(ModelForm):
    class Meta:
        model = Room
        
