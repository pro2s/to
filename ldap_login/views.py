# -*- coding: utf-8 -*-
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render, render_to_response, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


import sys
import ldap

def check_credentials(request, username, password):
   """Verifies credentials for username and password.
   Returns None on success or a string describing the error on failure
   # Adapt to your needs
   """
   LDAP_SERVER = 'ldap://10.1.0.50'
   # fully qualified AD user name
   LDAP_USERNAME = u'%s@elmotor.org' % username
   # your password
   LDAP_PASSWORD = password
   base_dn = 'DC=elmotor,DC=org'
   ldap_filter = u'userPrincipalName=%s@elmotor.org' % username
   attrs = ['memberOf']
   try:
       # build a client
       ldap_client = ldap.initialize(LDAP_SERVER)
       # perform a synchronous bind
       ldap_client.set_option(ldap.OPT_REFERRALS,0)
       ldap_client.simple_bind_s(LDAP_USERNAME.encode('ascii', 'replace'), LDAP_PASSWORD.encode('ascii', 'replace'))
   except ldap.INVALID_CREDENTIALS:
       ldap_client.unbind()
       request.session['login'] = ''
       return 'Wrong username or password'
   except ldap.SERVER_DOWN:
       request.session['login'] = ''
       return 'AD server not awailable'
   # all is well
   # get all user groups and store it in cerrypy session for future use
   request.session['login']=username
   #request.session[username] = str(ldap_client.search_s(base_dn,ldap.SCOPE_SUBTREE, ldap_filter, attrs)[0][1]['memberOf'])
   ldap_client.unbind()
   return None
   
def dologin(request):
    if 'exit' in request.GET:
        request.session['login'] = ''
        logout(request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    username = request.POST.get('username')
    password = request.POST.get('password')
   
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request,user)
            
    result = check_credentials(request,username, password)
    if result == None:
        print "OK"
    else:
        print result
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # Redirect after POST