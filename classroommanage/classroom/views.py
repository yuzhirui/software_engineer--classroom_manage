# -*- coding: utf-8 -*-
from django import forms
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from classroom.models import Building, Datetime, Room, Order
from classroom.forms import InqureForm, FreeroomForm, OrderForm, InformationForm, YourroomForm
import time

# home page
def home(request):
    if request.user.is_authenticated():
        name = request.user.username
    else:
        name = u'登录'
    return render_to_response("index.html", {'name': name})

#show the orders and rooms of a user
def order_room(request):
    if request.user.is_authenticated():
        name = request.user.username
        try:
            orders = Order.objects.filter(user__username__exact = name, is_dealed = False)
        except:
            orders = None
        orderforms = []
        if orders:
            for order in orders:
                orderforms.append(OrderForm(instance = order))
        roomforms = []
        rooms = Room.objects.filter(user__username__exact = name)
        if rooms:
            for room in rooms:
                roomforms.append(YourroomForm(instance = room))
        return render_to_response("yourcenter.html", {'name': name, 'orderforms': orderforms, \
        'roomforms': roomforms})
    return render_to_response("yourcenter.html", {'name': u'登录', 'orderforms':None, \
    'roomforms': None, 'msg': u'请登录进入个人中心'})

#update a user's information
def updateinform(request):
    if request.user.is_authenticated():
        name = request.user.username
        you = InformationForm(instance = request.user)
        if request.POST:
            you = InformationForm(request.POST)
            if you.is_valid():
                you.save()
                return render_to_response("update_inform.html", {'name': \
                request.user.ysername, 'msg': u'修改信息成功', 'you': you})
            else:
                return render_to_response("update_inform.html", {'name': \
                request.user.username, 'msg': u'输入信息有误', 'you': you})
        else:
            return render_to_response("update_inform.html", {'name': name, \
            'msg': u'修改个人信息', 'you': you})
    return render_to_response("update_inform.html", {'name': u'登录', \
    'msg': u'请登录来修改个人信息', 'you': None})  


# register an account
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/index/")
    else:
        form = UserCreationForm()
    return render_to_response("register.html", {'form': form})

#contact the admin
def contact(request):
    if request.user.is_authenticated():
        name = request.user.username
    else:
        name = u'登录'
    return render_to_response("contact.html", {'name': name})

#search the free room of a certain time
def inquire(request):
    if request.user.is_authenticated():
        name = request.user.username
    else:
        name = u'登录'

    ainqure = InqureForm( initial={'day': time.strftime('%Y-%m-%d',time.localtime(time.time()))} )
    if request.POST:
        ainqure = InqureForm(request.POST)
        if ainqure.is_valid():
            rooms = Room.inqureresults(ainqure)
            return render_to_response('inquire.html',
                    {
                        'name': name,
                        'rooms': rooms,
                        'inqure': ainqure,
                    })
        else:
            ainqure = InqureForm( initial={'day': time.strftime('%Y-%m-%d',time.localtime(time.time()))} )
            return render_to_response('inquire.html', {'name': name, 'inqure': ainqure})
    else:
        ainqure = InqureForm( initial={'day': time.strftime('%Y-%m-%d',time.localtime(time.time()))} )
        return render_to_response("inquire.html", {'name': name, 'inqure': ainqure})

#A user order rooms of a certain time
def appointment(request):
    if request.user.is_authenticated():
        name = request.user.username
        if request.POST:
            neworder = Order(user= request.user)
            order = OrderForm(request.POST, instance = neworder)
            if order.is_valid():
                order.save()
                return render_to_response('appointment.html', {'name': name, \
                'msg': u'提交申请成功', 'order': order})
            else:
                return render_to_response('appointment.html', {'name': name, \
                'msg': u'提交申请失败，请检查输入是否合法', 'order': order})
        order = OrderForm()
        return render_to_response('appointment.html', {'name': name, \
                'order': order})
            
    else:
        return render_to_response("appointment.html", {'name': u'登录', \
        'msg': u'您尚未登录，请登录后预约教室'})
