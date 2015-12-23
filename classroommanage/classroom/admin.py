# -*- coding: utf-8 -*-
from django.contrib import admin
from classroom.models import Room, Building, Order, Datetime, Useroom

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_dealed', 'is_agreed')
    search_fields = ('user', 'is_dealed')
    filter_horizontal = ('room',)
    
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'building','floor')
    search_fields = ('name',)
    
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'campus')
    search_fields = ('name',)
    
class DatetimeAdmin(admin.ModelAdmin):
    list_display = ('date', 'period')
    search_fields = ('date',)

class UseroomAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user', )
    list_filter = ('datetime',)

# Register your models here.
admin.site.register(Room, RoomAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Datetime, DatetimeAdmin)
admin.site.register(Useroom, UseroomAdmin)


