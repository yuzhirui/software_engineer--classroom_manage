# -*- coding: utf-8 -*-
from django.contrib import admin
from classroom.models import Room, Building, Order, Datetime

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_dealed', 'is_agreed')
# Register your models here.
admin.site.register(Room)
admin.site.register(Building)
admin.site.register(Order, OrderAdmin)
admin.site.register(Datetime)


