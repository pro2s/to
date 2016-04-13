# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from tasks.models import *

def check_login(view):
    def wrap(request, *args, **kwargs):
        user = checklogon(request)
        
        if user.view:
            kwargs["user"] = user
            return view(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/to/registration")
            
            
    return wrap

class User:
    auth = False
    view = False
    admin = False
    cehadmin = False
    id = 0
    username = ""
    login = ""
    cehuch = 0
    
    

def checklogon(request):
    user = User()
    
    if 'login' in request.session:
        user.login = request.session.get('login','');
        try:
            logeduser = RegistredUser.objects.get(login = user.login)     
        except RegistredUser.DoesNotExist:
            if user.login != "":
                logeduser = RegistredUser(name = user.login, login = user.login, cehuch = 0)
                logeduser.save()
            else:
                logeduser = None
                
        if logeduser:
            user.id = logeduser.id
            user.cehuch = logeduser.cehuch
            user.auth = True
            if logeduser.cehuch > 0:
                user.view = True

            user.username = logeduser.name
            try:
                isadmin = logeduser.roles.get(name='admin')
            except Role.DoesNotExist:                
                isadmin = None
                
            if isadmin:
                user.admin = True
                
    
    return user