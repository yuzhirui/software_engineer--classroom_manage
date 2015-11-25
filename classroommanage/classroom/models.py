# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from classroommanage import globalty
#from forms import InqureForm

class Building(models.Model):
    name = models.CharField(max_length = 30, verbose_name = u'教学楼')
    campus = models.CharField(max_length = 30, verbose_name = u'校区')

    def __unicode__(self):
        return self.name


class Datetime(models.Model):
    date = models.DateField(verbose_name = u'日期')
    period = models.IntegerField(max_length = 1, verbose_name = u'节次')

    def __unicode__(self):
        return u'%s 第%s' % (self.date, globalty.Period_list[self.period][1])

class Room(models.Model):
    name = models.CharField(max_length = 30, verbose_name = u'教室名称')
    building = models.ForeignKey(Building, verbose_name = u'教学楼')
    datetime = models.ForeignKey(Datetime, verbose_name = u'时间和节次')
    user = models.ForeignKey(User, null = True, blank = True, verbose_name = u'使用者')

    def __unicode__(self):
        return u'%s %s 第%s' % (self.name, self.datetime.date, globalty.Period_list[self.datetime.period][1])

    @staticmethod
    def inqureresults(inqure):
        if int(inqure['building'].value()) == 10:
            if int(inqure['campus'].value()) == 2:
                return Room.objects.filter(datetime__date__exact = inqure['day'].value(), \
                datetime__period__exact = int(inqure['period'].value()), user = None)
            return Room.objects.filter(building__campus__exact = globalty.Campus_list\
            [int(inqure['campus'].value())][1], datetime__date__exact = inqure['day'].value(), \
            datetime__period__exact = int(inqure['period'].value()), user = None)
        if int(inqure['campus'].value()) == 2:
            return Room.objects.filter(building__name__exact = globalty.Build_list\
            [int(inqure['building'].value())][1], datetime__date__exact = inqure['day'].value(), \
            datetime__period__exact = int(inqure['period'].value()), user = None)
        return Room.objects.filter(building__name__exact = globalty.Build_list\
        [int(inqure['building'].value())][1], building__campus__exact = \
        globalty.Campus_list[int(inqure['campus'].value())][1], datetime__date__exact = \
        inqure['day'].value(), datetime__period__exact = int(inqure['period'].value()), \
        user = None)

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name = u'用户')
    room = models.ManyToManyField(Room, verbose_name = u'教室以及时间')
    message = models.TextField(verbose_name = u'申请简述')
    is_dealed = models.BooleanField(verbose_name = u'是否处理了', default = False)
    is_agreed = models.BooleanField(verbose_name = u'是否同意了', default = False)

    def __unicode__(self):
        return u'%s %s %s %s%s' % (self.id, self.user.username, u'申请:', self.room.all()[0], u'(等)')

    def autodeal(self, is_agree):
        if is_agree:
            self.is_agreed = True
            self.is_dealed = True
            for room in self.room.all():
                room.user = self.user
                room.save()
        else:
            self.is_dealed = True
        self.save()
    
