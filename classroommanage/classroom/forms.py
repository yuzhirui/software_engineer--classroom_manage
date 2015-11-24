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
        
class ChangepwdForm(forms.Form):
    oldpassword = forms.CharField(
        required=True,
        label=u"原密码",
        error_messages={'required': u'请输入原密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"原密码",
            }
        ),
    ) 
    newpassword1 = forms.CharField(
        required=True,
        label=u"新密码",
        error_messages={'required': u'请输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"新密码",
            }
        ),
    )
    newpassword2 = forms.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required': u'请再次输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"确认密码",
            }
        ),
     )
    def clean(self):
       if not self.is_valid():
           raise forms.ValidationError(u"所有项都为必填项")
       elif self.cleaned_data['newpassword1'] <> self.cleaned_data['newpassword2']:
           raise forms.ValidationError(u"两次输入的新密码不一样")
       else:
           cleaned_data = super(ChangepwdForm, self).clean()
       return cleaned_data
