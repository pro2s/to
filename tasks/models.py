# -*- coding: utf-8 -*-
from django.db import models
from elmotor.models import Naimceh

class Role(models.Model):
    name = models.CharField(max_length=50)
    view_name = models.CharField(max_length=50)
    def __unicode__(self):
        return u'%s' % (self.view_name)
    
class RegistredUser (models.Model):
    name = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    cehuch = models.IntegerField()
    tn = models.IntegerField(null=True, blank=True)
    roles = models.ManyToManyField(Role, null=True, blank=True)
    def __unicode__(self) :
        return u'%s' % self.name        
    @property
    def dev(self):
        ceh = {}
        _cehuch = abs(self.cehuch)
        cehuch = Naimceh.objects.using('elmotor').get(cehuch = _cehuch)
        ceh["uch_name"] = cehuch.name
        ceh["uch"] = cehuch.uch 
        dbceh = Naimceh.objects.using('elmotor').get(ceh = cehuch.ceh,uch = 0)
        ceh["ceh_name"] = dbceh.name
        ceh["ceh"] = dbceh.ceh
        return ceh
        
class Status(models.Model):
    name = models.CharField(max_length=20)
    view_name = models.CharField(max_length=20)
    close_task = models.BooleanField()
    def __unicode__(self):
        return u'%s' % (self.view_name)
    
class UserTask(models.Model):
    parrent  = models.ForeignKey("UserTask", null=True, blank=True)
    owner  = models.ForeignKey(RegistredUser, related_name="mytasks", related_query_name="mytask")
    doer  = models.ForeignKey(RegistredUser, related_name="tasks", related_query_name="task", null=True, blank=True)
    cehuch = models.IntegerField()
    task_num = models.CharField(max_length=10, null=True, blank=True)
    task_date = models.DateField(null=True, blank=True)
    date_start = models.DateField(auto_now_add=True)
    date_done = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=120)
    desc = models.TextField()
    progress = models.IntegerField(default = 0)
    order = models.IntegerField(default = 0)
    statuses = models.ManyToManyField(Status, through='UserTaskStatus')
    @property
    def status(self):
        last = self.usertaskstatus_set.last()
        return last.status
        
class UserTaskStatus(models.Model):
    task  = models.ForeignKey(UserTask)
    status = models.ForeignKey(Status)
    date  = models.DateField(auto_now=True)
    user  = models.ForeignKey(RegistredUser)
    reason = models.CharField(max_length=120, null=True, blank=True)

