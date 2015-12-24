# -*- coding: utf-8 -*-
from django import forms
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import auth
#from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, get_object_or_404
from classroom.models import Building, Datetime, Room, Order, Useroom
from classroom.forms import InqureForm, FreeroomForm, OrderForm, InformationForm, \
        YourroomForm, ChangepwdForm
import time
import datetime
from classroommanage import globalty
import json
import random

# home page
def home(request):
    isin = False
    if request.user.is_authenticated():
        name = request.user.username
        isin = True
    else:
        name = u'登录'
    return render_to_response("index.html", {'name': name, 'isin': isin})

def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
    # Correct password, and the user is marked "active"
        auth.login(request, user)
        if user.is_staff:
            return render_to_response("admin.html")
    # Redirect to a success page.
        return HttpResponseRedirect("/index")
    else:
    # Show an error page
        return render_to_response("login.html")

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
                tho = Order.objects.get(id = request.POST.get('y'))
                tho.autodeal(True)
                subject = u'管理员同意了您的预约'
                mail = tho.user.email
                message = tho.user.username + u'您好！管理员已经批准了您的预约。您可以登录网站查看。\
                预约内容为' + tho.output() + u'使用时间为' + tho.datetime.output()
                
            else:
                tho = Order.objects.get(id = request.POST.get('n'))
                tho.autodeal(False)
                subject = u'管理员拒绝了您的预约'
                mail = tho.user.email
                message = tho.user.username + u'您好！很抱歉，管理员拒绝了您的预约。\
                预约内容为' + tho.output() + u'使用时间为' + tho.datetime.output()
                
            send_mail(subject, message, '18994855609@163.com', [mail], fail_silently=False)
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
        if request.POST:
            oid = request.POST['d']
            Order.objects.get(id = oid).delete()
            subject = request.user.username + u'取消预约'
            message = u'用户取消了该预约申请。'
            send_mail(subject, message, '18994855609@163.com', ['2927379969@qq.com'], fail_silently=True)
        lst = Useroom.objects.filter(user__username__exact = name)
        return render_to_response("yourcenter.html", {'name': name, 'orders': orders, \
        'roomforms': lst, 'isin': isin})
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
            you = InformationForm(request.POST, instance = request.user)
            if you.is_valid():
                you.save()
                if request.user.is_staff:
                    return render_to_response("adminupdate_inform.html", {'name': \
                    request.user.username, 'msg': u'修改信息成功', 'you': you})
                return render_to_response("update_inform.html", {'name': \
                    request.user.username, 'msg': u'修改信息成功', 'you': you, 'isin': isin})
            else:
                if request.user.is_staff:
                    return render_to_response("adminupdate_inform.html", {'name': \
                    request.user.username, 'msg': u'输入信息有误', 'you': you})
                return render_to_response("update_inform.html", {'name': \
                request.user.username, 'msg': u'输入信息有误', 'you': you, 'isin': isin})
        else:
            if request.user.is_staff:
                return render_to_response("adminupdate_inform.html", {'name': \
                request.user.username, 'msg': u'修改个人信息', 'you': you})
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
                    if request.user.is_staff:
                        return render_to_response('index.html', {'changepwd_success':True})
                    return render_to_response('index.html', {'changepwd_success':True, \
                    'isin': isin, 'name': name})
                else:
                    if request.user.is_staff:
                        return render_to_response('adminchangepwd.html',{'form': form,\
                    'oldpassword_is_wrong':True})
                    return render_to_response('changepwd.html', {'form': form,\
                    'oldpassword_is_wrong':True, 'isin': isin, 'name': name})
        if request.user.is_staff:
            return render_to_response('adminchangepwd.html',{'form': form})
        return render_to_response('changepwd.html', {'form': form, 'isin': isin, 'name': name})
    else:
        return render_to_response('changepwd.html', {'form': form, 'isin': isin, 'name': u'登录'})

#contact the admin
def contact(request):
    isin = False
    if request.user.is_authenticated():
        isin = True
        name = request.user.username
        if request.POST:
            message = request.POST['message']
            if request.user.get_full_name():
                subject = request.POST['subject'] + u' 来自'+ request.user.get_full_name() + u'的邮件'
            else:
                subject = request.POST['subject'] + u' 来自'+ request.user.username + u'的邮件'
            send_mail(subject, message, '18994855609@163.com', ['2927379969@qq.com'], fail_silently=False)
            return render_to_response("contact.html", {'name': name, 'isin': isin, 'msg': u'发送成功！'})
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
    if request.POST:
        ainqure = InqureForm(request.POST)
        try:
            rooname = request.POST['mroom']            
            roos = Room.objects.filter(name__icontains = rooname)
        except:
            roos = []
        if roos:
            days = []
            for i in range(7):
                d1 = datetime.datetime.now()
                d2 = d1 + datetime.timedelta(days = i)
                day = str(d2).split()[0]
                days.append(day)
            tabs = []
            n = len(roos)
            for i in range(n):
                tabs.append([])
                tabs[i].append(roos[i])
                for j in range(7):
                    for k in range(5):
                        datet = Datetime.objects.get(date = days[j], period = k)
                        user = Useroom.objects.get(datetime = datet, room = roos[i]).user
                        tabs[i].append(user)
        else:
            tabs = None
            days = None
        if ainqure.is_valid():
            rooms = None
            rooms = Useroom.inqureresults(ainqure)
            dat = ainqure['day'].value()
            peri = ainqure['period'].value()
            datetim = Datetime.objects.get(date = dat, period = peri).id
            return render_to_response('inquire.html',
                    {
                        'name': name,
                        'rooms': rooms,
                        'inqure': ainqure,
                        'isin': isin,
                        'datetime': datetim,
                        'tabs': tabs,
                        'days': days,
                    })
        else:
            ainqure = InqureForm(request.POST)
            return render_to_response('inquire.html', {'name': name, 'inqure': ainqure, 'isin': isin,\
            'msg': u"查询无结果", 'tabs': tabs, 'days': days})
    else:
        ainqure = InqureForm()
        return render_to_response("inquire.html", {'name': name, 'inqure': ainqure, 'isin': isin})

#A user order rooms of a certain time
def appointment(request):
    isin = False
    if request.user.is_authenticated():
        isin = True
        name = request.user.username
        neworder = Order(user= request.user)
        try:
            two = request.GET['q'].split()
            roomid = int(two[0])
            did = int(two[1])
            neworder.datetime = Datetime.objects.get(id=did)
            theroom = Room.objects.get(id=roomid)
        except:
            theroom = None
        if request.POST:
            if not theroom:
                 return render_to_response('appointment.html', {'name': name, \
                'msg': u'您尚未选择任何教室，请先查询再预约', 'isin': isin})
            message = request.POST['message']
            if len(message) > 10:
                neworder.message = message
                neworder.save()
                neworder.room.add(theroom)
                subject = request.user.username + u'用户预约教室'
                send_mail(subject, message, '18994855609@163.com', ['2927379969@qq.com'], fail_silently=True)
                return render_to_response('appointment.html', {'name': name, \
                'msg': u'提交申请成功', 'isin': isin})
            else:
                return render_to_response('appointment.html', {'name': name, \
                'msg': u'提交申请失败，简述字数不应少于10个字', 'isin': isin})
        return render_to_response('appointment.html', {'name': name, 'isin': isin })
            
    else:
        return render_to_response("appointment.html", {'name': u'登录', \
        'msg': u'您尚未登录，请登录后预约教室', 'isin': isin})

def forget(request):
    msg = ''
    if request.POST:
        name = request.POST['username']
        mail = request.POST['email']
        msg = u'修改密码成功，请查收邮件获取新密码！'
        try:
            user = User.objects.get(username = name, email = mail)
            new = str(random.randint(100000, 999999))
            user.set_password(new)
            user.save()
            subject = name + u'重置密码'
            message = u'新密码为:'+ new + u'，请登录后尽快修改密码!'
            send_mail(subject, message, '18994855609@163.com', [mail], fail_silently=True)
        except:
            msg = u'输入信息有误，请重试！'
    return render_to_response("forget.html", {'msg': msg})

def task(request):
    try:
        for i in range(7):
            d1 = datetime.datetime.now()
            d2 = d1 + datetime.timedelta(days = i)
            day = str(d2).split()[0]
            dates = Datetime.objects.filter(date = day)
            if not dates:
                for j in range(5):
                    thedate = Datetime(date = day, period = j)
                    thedate.save()
                    rooms = Room.objects.all()
                    for room in rooms:
                        tab = Useroom()
                        tab.room = room
                        tab.datetime = thedate
                        tab.save()
        return render_to_response("task.html", {'msg': u'添加成功'})
    except:
        return render_to_response("task.html", {'msg': u'添加失败，请重试'})

def bui(request):
    n = int(request.GET['n'])
    build = ''
    if n == 1:
        build = u'<option value="0">正心楼</option>  <option value="1">诚意楼</option> \
        <option value="2">格物楼</option>  <option value="3">致知楼</option>  \
        <option value="4">电机楼</option>  <option value="5">机械楼</option>'
    elif n == 2:
        build = u'<option value="6">主楼</option>  <option value="7">东配楼</option>\
        <option value="8">西配楼</option>  <option value="9">青年公寓</option>'
    else:
        build = u'<option value="0">正心楼</option>  <option value="1">诚意楼</option> \
        <option value="2">格物楼</option>  <option value="3">致知楼</option>  \
        <option value="4">电机楼</option>  <option value="5">机械楼</option> \
        <option value="6">主楼</option>  <option value="7">东配楼</option>\
        <option value="8">西配楼</option>  <option value="9">青年公寓</option>'
    return HttpResponse(json.dumps(build), content_type='application/json')

def buil(request):
    n = int(request.GET['n'])
    build = u'<option value="0">正心楼</option>  <option value="1">诚意楼</option> \
        <option value="2">格物楼</option>  <option value="3">致知楼</option>  \
        <option value="4">电机楼</option>  <option value="5">机械楼</option> \
        <option value="6">主楼</option>  <option value="7">东配楼</option>\
        <option value="8">西配楼</option>  <option value="9">青年公寓</option>\
        <option value="10">全部</option>'
    if n == 1:
        build = u'<option value="0">正心楼</option>  <option value="1">诚意楼</option> \
        <option value="2">格物楼</option>  <option value="3">致知楼</option>  \
        <option value="4">电机楼</option>  <option value="5">机械楼</option>\
        <option value="10">全部</option>'
    elif n == 2:
        build = u'<option value="6">主楼</option>  <option value="7">东配楼</option>\
        <option value="8">西配楼</option>  <option value="9">青年公寓</option>\
        <option value="10">全部</option>'
    return HttpResponse(json.dumps(build), content_type='application/json')

def flo(request):
    n = int(request.GET['build'])
    floors = ''
    if n == 0 or n == 6 or n == 9:
        floors = u'<option value="0">一楼</option> <option value="1">二楼</option> \
        <option value="2">三楼</option> <option value="3">四楼</option> \
        <option value="4">五楼</option> <option value="5">六楼</option> \
        <option value="6">七楼</option> <option value="7">八楼</option>\
        <option value="8">九楼</option>'
    elif n == 1 or n == 7 or n == 8:
        floors = u'<option value="0">一楼</option> <option value="1">二楼</option> \
        <option value="2">三楼</option> <option value="3">四楼</option> \
        <option value="4">五楼</option> <option value="5">六楼</option>'
    elif n == 2:
        floors = u'<option value="0">一楼</option> <option value="1">二楼</option> \
        <option value="2">三楼</option> <option value="3">四楼</option> \
        <option value="4">五楼</option> <option value="5">六楼</option> \
        <option value="6">七楼</option> <option value="7">八楼</option>'
    elif n == 3 or n == 4 or n == 5:
        floors = u'<option value="0">一楼</option> <option value="1">二楼</option> \
        <option value="2">三楼</option> <option value="3">四楼</option>'
    return HttpResponse(json.dumps(floors), content_type='application/json')
 
    
def inq(request):
    build = int(request.GET['build'])
    flo = int(request.GET['floor']) + 1
    day = request.GET['day']
    per = int(request.GET['period'])
    bui = Building.objects.get(name = globalty.Build_list[build][1])
    rooms = Room.objects.filter(building = bui, floor = flo)
    s = ''
    names = []
    datet = Datetime.objects.get(date = day, period = per)
    for room in rooms:
        tab = Useroom.objects.get(room = room, datetime = datet)
        names.append(room.name)
        if tab.user:
            s += 'a'
        else:
            s += 'c'
    maps = [s, names]
    return HttpResponse(json.dumps(maps), content_type='application/json')

def submit(request):
    rooms = request.GET['rooms']
    day = request.GET['day']
    per = int(request.GET['period'])
    message = request.GET['message']
    datet = Datetime.objects.get(date = day, period = per)
    try:
        order = Order(user = request.user, datetime = datet, message = message)
        order.save()
        rs = rooms.split()
        for rm in rs:
            order.room.add(Room.objects.get(name = rm))
        is_ok = True
    except:
        is_ok = False
    subject = request.user.username + u'用户预约教室'
    send_mail(subject, message, '18994855609@163.com', ['2927379969@qq.com'], fail_silently=True)
    return HttpResponse(json.dumps(is_ok), content_type='application/json')
