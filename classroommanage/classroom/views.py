# -*- coding: utf-8 -*-
from django import forms
from django.contrib import auth
#from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from classroom.models import Building, Datetime, Room, Order
from classroom.forms import InqureForm, FreeroomForm, OrderForm, InformationForm, \
        YourroomForm, ChangepwdForm
import time

# home page
def home(request):
    isin = False
    if request.user.is_authenticated():
        name = request.user.username
        isin = True
    else:
        name = u'登录'
    return render_to_response("index.html", {'name': name, 'isin': isin})

def admindisplay(request):
    is_super = False
    if request.user.is_staff:
        is_super = True
        try:
            orders = Order.objects.filter(is_dealed = False)
        except:
            orders = None
        if request.POST:
            if request.POST.get('y'):
                Order.objects.get(id = request.POST.get('y')).autodeal(True)
            else:
                Order.objects.get(id = request.POST.get('n')).autodeal(False)
        return render_to_response("admindisplay.html", {'is_super': is_super, \
        'orders': orders, 'name': u'管理员', 'isin': True})
    else:
        return render_to_response("index.html", {'name': u'登录', 'isin': False,\
        'is_super': is_super})
        
def orderdetails(request):
    is_super = False
    if request.user.is_staff:
        is_super = True
        num = request.GET['q']
        theorder = get_object_or_404(Order, id = num)
        rooms = theorder.room.all()
        if request.POST:
            if request.POST.get('y'):
                Order.objects.get(id = request.POST.get('y')).autodeal(True)
            else:
                Order.objects.get(id = request.POST.get('n')).autodeal(False)
        return render_to_response("orderdetails.html", {'is_super': is_super, \
        'theorder': theorder, 'rooms': rooms, 'name': u'管理员', 'isin': True})
    else:
        return render_to_response("index.html", {'name': u'登录', 'isin': False, 'is_super': is_super})

#show the orders and rooms of a user
def order_room(request):
    isin = False
    if request.user.is_authenticated():
        name = request.user.username
        isin = True
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
        'roomforms': roomforms, 'isin': isin})
    return render_to_response("yourcenter.html", {'name': u'登录', 'orderforms':None, \
    'roomforms': None, 'msg': u'请登录进入个人中心', 'isin': isin})

#update a user's information
def updateinform(request):
    isin = False
    if request.user.is_authenticated():
        isin = True
        name = request.user.username
        you = InformationForm(instance = request.user)
        if request.POST:
            you = InformationForm(request.POST)
            if you.is_valid():
                you.save()
                return render_to_response("update_inform.html", {'name': \
                request.user.ysername, 'msg': u'修改信息成功', 'you': you, 'isin': isin})
            else:
                return render_to_response("update_inform.html", {'name': \
                request.user.username, 'msg': u'输入信息有误', 'you': you, 'isin': isin})
        else:
            return render_to_response("update_inform.html", {'name': name, \
            'msg': u'修改个人信息', 'you': you, 'isin': isin})
    return render_to_response("update_inform.html", {'name': u'登录', \
    'msg': u'请登录来修改个人信息', 'you': None, 'isin': isin})  


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

def changepwd(request):
    isin = False
    if request.user.is_authenticated():
        isin = True
        name = request.user.username
        form = ChangepwdForm()
        if request.POST:
            form = ChangepwdForm(request.POST)
            if form.is_valid():
                username = request.user.username
                oldpassword = request.POST.get('oldpassword', '')
                user = auth.authenticate(username=username, password=oldpassword)
                if user is not None and user.is_active:
                    newpassword = request.POST.get('newpassword1', '')
                    user.set_password(newpassword)
                    user.save()
                    return render_to_response('index.html', {'changepwd_success':True, \
                    'isin': isin, 'name': name})
                else:
                    return render_to_response('changepwd.html', {'form': form,\
                    'oldpassword_is_wrong':True, 'isin': isin, 'name': name})
            else:
                return render_to_response('changepwd.html', {'form': form, 'isin': isin, 'name': name})
        return render_to_response('changepwd.html', {'form': form, 'isin': isin, 'name': name})
    else:
        return render_to_response('changepwd.html', {'form': form, 'isin': isin, 'name': u'登录'})

#contact the admin
def contact(request):
    isin = False
    if request.user.is_authenticated():
        isin = True
        name = request.user.username
    else:
        name = u'登录'
    return render_to_response("contact.html", {'name': name, 'isin': isin})

#search the free room of a certain time
def inquire(request):
    isin = False
    if request.user.is_authenticated():
        isin = True
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
                        'isin': isin,
                    })
        else:
            ainqure = InqureForm( initial={'day': time.strftime('%Y-%m-%d',time.localtime(time.time()))} )
            return render_to_response('inquire.html', {'name': name, 'inqure': ainqure, 'isin': isin})
    else:
        ainqure = InqureForm( initial={'day': time.strftime('%Y-%m-%d',time.localtime(time.time()))} )
        return render_to_response("inquire.html", {'name': name, 'inqure': ainqure, 'isin': isin})

#A user order rooms of a certain time
def appointment(request):
    isin = False
    if request.user.is_authenticated():
        isin = True
        name = request.user.username
        if request.POST:
            neworder = Order(user= request.user)
            order = OrderForm(request.POST, instance = neworder)
            if order.is_valid():
                order.save()
                return render_to_response('appointment.html', {'name': name, \
                'msg': u'提交申请成功', 'order': order, 'isin': isin})
            else:
                return render_to_response('appointment.html', {'name': name, \
                'msg': u'提交申请失败，请检查输入是否合法', 'order': order, 'isin': isin})
        order = OrderForm()
        return render_to_response('appointment.html', {'name': name, \
                'order': order, 'isin': isin})
            
    else:
        return render_to_response("appointment.html", {'name': u'登录', \
        'msg': u'您尚未登录，请登录后预约教室', 'isin': isin})
