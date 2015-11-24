# -*- coding: utf-8 -*-
from django.contrib import admin
from classroom.models import Room, Building, Order, Datetime

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_dealed', 'is_agreed')
    search_fields = ('user', 'is_dealed')
    filter_horizontal = ('room',)
    
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'building', 'user')
    search_fields = ('name',)
    list_filter = ('datetime',)
    
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'campus')
    search_fields = ('name',)
    
class DatetimeAdmin(admin.ModelAdmin):
    list_display = ('date', 'period')
    search_fields = ('date',)

# Register your models here.
admin.site.register(Room, RoomAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Datetime, DatetimeAdmin)


