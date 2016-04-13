# -*- coding: utf-8 -*-
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render, render_to_response, get_object_or_404, HttpResponseRedirect
from tasks.models import *
from auth import checklogon

@csrf_protect
def index(request):
    user = checklogon(request)            
    
    c = {
    'title': 'MEZ',
    'user':user,
    }
    return render(request, 'dashboard/index.html', c)
     
