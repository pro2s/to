# -*- coding: utf-8 -*-
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render, render_to_response, get_object_or_404, HttpResponseRedirect
from tasks.models import *
from auth import checklogon
from django.db.models import Q
from elmotor.models import Tncehfio, Naimceh


def doregistration(request):
    user = checklogon(request)    
    error = ""
    try:
        reguser = RegistredUser.objects.get(login = user.login)     
    except RegistredUser.DoesNotExist:
        reguser = None

    if reguser:        
        username = request.POST.get('username','')
        
        try:
            tn = int(request.POST.get('tn',0))
        except:
            tn  = None
        
        try:
            ceh = int(request.POST.get('ceh',0))
        except:
            error =  "Не введен цех/участок"
            ceh = -1 
            
        try:            
            cehuch = int(request.POST.get('cehuch',0))
        except:
            cehuch = 0 
        
        if tn > 0 and tn < 7000:
            
            try:
                tnfio = Tncehfio.objects.get(tn = tn)     
            except Tncehfio.DoesNotExist:
                tnfio = None
            
            if tnfio:
                reguser.tn = tn
                username  = "%s %s. %s." % (tnfio.fm.capitalize(), tnfio.im[0], tnfio.ot[0])
                cehuch = tnfio.ceh * 100 + tnfio.uch

        if cehuch == 0 and ceh > 0:
            cehuch = ceh * 100
        if username != '':
            reguser.name = username
                
        if error == "":
            cehuch = -1 * abs(int(cehuch))
            reguser.cehuch = cehuch
            reguser.save()
        else:
            registration(request, error)
            
    return HttpResponseRedirect("/to/registration")
    
    

@csrf_protect
def registration(request, error = ""):
    user = checklogon(request)            
    if user.view:
        return HttpResponseRedirect("/to/")
    cehs = Naimceh.objects.filter(~Q(name__contains='(Н/С)'), uch=0).all()
    uchs = Naimceh.objects.filter(~Q(name__contains='(Н/С)'), uch__gt=0).all()
    
    c = {
    'error': error,
    'title': 'Регистрация',
    'user':user,
    'cehs':cehs,
    'uchs':uchs,
    }
    
    return render(request, 'auth/registration.html', c)
     
    
    