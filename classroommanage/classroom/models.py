from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=30)
    campus = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=30)
    building = models.ForeignKey(Building)

    def __unicode__(self):
        return self.name

class Time(models.Model):
    name = models.CharField(max_length=30)
    current_date = models.DateField()
    rooms_open = models.ManyToManyField(Room)

    def __unicode__(self):
        return u'%s %s' % (self.current_date, self.name)
