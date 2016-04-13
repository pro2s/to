from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'to.views.home', name='home'),
    # url(r'^it/', include('to.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', 'dashboard.views.index'),   
    (r'^login$', 'ldap_login.views.dologin'),  
    (r'^about/$', 'tasks.views.about'),
    (r'^users/$', 'tasks.views.users'),
    (r'^file$', 'tasks.views.file'),
    (r'^task$', 'tasks.views.task'),
    (r'^task/(?P<id>[0-9]+)$', 'tasks.views.viewtask'),
    (r'^newtask$', 'tasks.views.edittask',  {'mode': 'new'}),
    (r'^edittask$', 'tasks.views.edittask'),
    (r'^deltask$', 'tasks.views.deltask'),
    (r'^savetask$', 'tasks.views.savetask' ),
    (r'^users/reguser$', 'tasks.views.reguser'),
    (r'^users/del$', 'tasks.views.deluser'),
    (r'^tasks/$', 'tasks.views.tasks'),
    (r'^mytasks/$', 'tasks.views.tasks',  {'mode': 'user'}),
    (r'^cehtasks/$', 'tasks.views.tasks',  {'mode': 'ceh'}),
    (r'^registration/$', 'auth.views.registration'),
    (r'^doregistration$', 'auth.views.doregistration'),  
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
)
