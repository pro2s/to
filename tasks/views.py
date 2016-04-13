# -*- coding: utf-8 -*-
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render, render_to_response, get_object_or_404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from elmotor.models import Tncehfio, Naimceh
from tasks.models import *
from auth import check_login
from django.db.models import Q
from datetime import datetime
import re
import tempfile
import shutil
import glob
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import json
import codecs

FILE_UPLOAD_DIR = '/var/www/django/to/media'

def getdate(s_date):
    """Проверка даты с разными форматами ввода"""
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d.%m.%y','%d/%m/%y'):
        try:
            return datetime.strptime(s_date, fmt)
        except ValueError:
            pass
    return None

    
def get_cehname():
    """Генерирует список сокращенных названий цеха
    Если есть сокращенное название цеха в скобках после имени 
    Или сокращение первых трех слов больше 1 символа до 5 букв.
    """
    cehuch = Naimceh.objects.all()
    cehname = {}
    for ceh in cehuch:
        p = re.compile('.*\((.*?)\)')
        m  = p.match(ceh.name)
        if m:
            name = m.group(1)
        else:
            name = None
        if name:
            cehname[ceh.cehuch] = name
        else:
            ceh_words = ceh.name.split(" ")
            _ceh_words = []
            count = 2
            for word in ceh_words:
                if len(word) > 5:
                    _ceh_words.append(word[0:4] + ".") 
                else:
                    _ceh_words.append(word) 
                if len(word) == 1:
                    count+=1
                if len(_ceh_words) > count:
                    break
            cehname[ceh.cehuch] = " ".join(_ceh_words)
    
    return cehname

    
def list_paginator(count,list,page):
    """Предварительная обработка спика пагинатором"""
    paginator = Paginator(list, count)
    page_i = 1
    try:
        docs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        docs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        docs = paginator.page(paginator.num_pages)
    if page != None: 
        page_i = int(page)
    if docs.has_next():
        next_page = paginator.page(page_i+1) 
    if page_i > 1:
        prev_page = paginator.page(page_i-1) 
    return docs
    
def get_task_files(task_id):
    """Получение файлов для задачи"""
    if task_id is None or task_id == 0:
        return {}
    result = {}
    prefix = "%d__" % task_id
    files = glob.glob(FILE_UPLOAD_DIR + "/" + prefix + "*.*")
    for file in files:
        name = os.path.basename(file)
        result[name[len(prefix):]] = name
    return result
     
def handle_uploaded_file(task_id, source):
    """Сохранение файла"""
    dest =  FILE_UPLOAD_DIR + u'/%d__%s' % (task_id, source.name)
    path = default_storage.save(dest, ContentFile(source.read()))
    return path

def about(request):
    """О системе"""
    changes = {}
    path = settings.BASE_DIR + '/it/changes.json'
    with codecs.open(path, "r", "utf-8") as data:    
        changes = json.load(data)
    
    c = {
    'title': 'О системе',
    'changes': changes,
    }
    
    return render(request, 'tasks/about.html', c)


@check_login
@csrf_protect
def users(request, user):
    """Выводит список пользователей"""
    dbusers = RegistredUser.objects.all()        
    
    c = {
    'title': 'Пользователи',
    'user': user,
    'users':dbusers,
    }
    
    return render(request, 'tasks/users.html', c)
     

@check_login
def deluser(request, user):
    """Удаление пользователя"""
    id = request.GET.get('id',0)
    
    if id != 0:
        try:
            reguser = RegistredUser.objects.get(pk = id)     
        except RegistredUser.DoesNotExist:
            reguser = None
        
        if (reguser and user.admin):         
            reguser.delete()
            
    return HttpResponseRedirect("/to/users")

@check_login
def reguser(request, user):
    """Регистрация пользователя"""
    id = request.GET.get('id',0)
    
    if id != 0:
        try:
            reguser = RegistredUser.objects.get(pk = id)     
        except RegistredUser.DoesNotExist:
            reguser = None
        
        if reguser and (user.admin or (user.cehadmin and user.cehuch / 100 == reguser.cehuch / 100)):         
            reguser.cehuch = abs(reguser.cehuch)
            reguser.save()
            
    return HttpResponseRedirect("/to/users")
    
@check_login
def task(request, user):
    """Изменение статуса задачи"""
    id = request.GET.get('id',0)
    status = request.GET.get('status','')
    if id != 0:
        dbtask = None
        try:
            dbtask = UserTask.objects.get(pk = id)     
        except UserTask.DoesNotExist:
            dbtask = None
        if dbtask and (user.admin or user.cehuch == dbtask.cehuch or  (user.cehuch % 100 == 0 and user.cehuch / 100 == dbtask.cehuch / 100) or dbtask.doer_id == user.id  or dbtask.owner_id == user.id):      
            present = datetime.now()

            if dbtask.date_done and present < dbtask.date_done:
                # Redirect to form for input reason
                pass
            if status != "":
                status = Status.objects.get(name = status)
                taskstatus  = UserTaskStatus(task = dbtask, status = status, user_id = user.id, reason ="");
                taskstatus.save();
                
            
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # Redirect after POST
    
  
@check_login     
@csrf_protect
def tasks(request, user, mode = "all"):
    """Вывод задач"""
    title = "Задачи"
    _tasks = []
    if mode == "all":
        title = "Все здачи"
        dbtasks = UserTask.objects.filter(parrent = None).all()
    if mode == "user":    
        title = "Задачи пользователя"    
        dbtasks = UserTask.objects.filter(doer__pk = user.id).all()
    if mode == "ceh":        
        title = "Задачи подразделения"    
        dbtasks = UserTask.objects.filter(cehuch__gte = user.cehuch - user.cehuch % 100,cehuch__lt = user.cehuch - user.cehuch % 100 + 100).all()
    
    
    ptasks =  list_paginator(5, dbtasks, request.GET.get('page'))
    for task in ptasks:
        data = {}
        subtasks = {}
        subtasks_tmp = UserTask.objects.filter(parrent = task).all()
        files = get_task_files(task.id)
        for subtask in subtasks_tmp:
            cehuch = subtask.cehuch
            ceh  = cehuch / 100 * 100
            if ceh not in subtasks:
                subtasks[ceh] = {}
            if cehuch not in subtasks[ceh]:
                subtasks[ceh][cehuch] = []

            subtasks[ceh][cehuch].append(subtask)
        
        data["data"] = task         
        data["subtasks"] = subtasks
        data["files"] = files
        _tasks.append(data)
        
    cehname = get_cehname()
        
    c = {
    'title': title,
    'tasksmode': mode,
    'user':user,
    'cehname': cehname,
    'tasks': _tasks,
    'ptasks': ptasks,
    }
    return render(request, 'tasks/tasks.html', c)
     
@check_login     
@csrf_protect
def viewtask(request, user, id = 0):
    """Просмотр задачи"""
    task = None
    subtask = None
    files = []
    if id != 0:
        try:
            task = UserTask.objects.get(pk = id)     
            subtask = UserTask.objects.filter(parrent_id = id).all()
            files = get_task_files(task.id)
        except UserTask.DoesNotExist:
            task = None
    
            
    cehname = get_cehname()
    
    cehuch = dict((x.cehuch, x.name) for x in Naimceh.objects.all())
    
    c = {
    'title': 'Задача',
    'cehname': cehname,
    'cehuch':cehuch,
    'user': user,
    'task': task,
    'subtask':subtask,
    'files': files,
    }
    return render(request, 'tasks/task.html', c)
     
@check_login     
@csrf_protect
def edittask(request, user, mode = "edit"):
    """Информация для формы редактирования"""
    
    id = request.GET.get('id',0)
    parrent = request.GET.get('parrent',0)
    title = "Редактировать задачу"
    
    if parrent != 0:
        title = "Редактировать подзадачу"
            
    task = None
    subtask = None
    if id != 0:
        try:
            task = UserTask.objects.get(pk = id)   
            subtask = UserTask.objects.filter(parrent_id = id).all()
        except UserTask.DoesNotExist:
            task = None
            
    
    if mode == "new":
        title = "Новая задача"
        if parrent != 0:
            title = "Новая подзадача"
    cehname = get_cehname()        
    cehs = Naimceh.objects.filter(~Q(name__contains='(Н/С)'), uch=0).all()
    uchs = Naimceh.objects.filter(~Q(name__contains='(Н/С)'), uch__gt=0).all()
    users = RegistredUser.objects.all()
    
    back_url = '/to/tasks'
    files = {}
    if task != None:
        files = get_task_files(task.id)
        if task.parrent != None:
            back_url = '/to/edittask?id=%d' % task.parrent_id
        
            
    
    c = {
    'title': title,
    'cehname': cehname,
    'cehs':cehs,
    'uchs':uchs,
    'user': user,
    'users':users,
    'task': task,
    'files': files,
    'mode':mode,
    'subtask':subtask,
    'parrent':parrent,
    'return':back_url,
    }
    
    return render(request, 'tasks/form.html', c)

    
@check_login     
@csrf_protect
def savetask(request, user):
    """Сохранение задачи"""
    id = request.GET.get('id','')
    mode = request.GET.get('mode','edit')
    
    if id == '':
        id = request.POST.get('id','')
    parrent = request.POST.get('parrent','')
    doer  = request.POST.get('doer', '')
    ceh = request.POST.get('ceh','')
    cehuch = request.POST.get('cehuch','')
    task_num = request.POST.get('task_num','')
    task_date =  getdate(request.POST.get('task_date',''))
    date_start = getdate(request.POST.get('date_start',''))
    date_end = getdate(request.POST.get('date_end', ''))
    
    title = request.POST.get('title','')
    desc = request.POST.get('desc','')
    
    if parrent == '':
        parrent = None
    else:
        parrent = int(parrent)
        
    if doer == '':
        doer = None
        
    if cehuch == '':
        cehuch = int(ceh) * 100

    task = None
    subtask = None
    if id != "" and mode != "new" :
        try:
            task = UserTask.objects.get(pk = id)   
            subtask = UserTask.objects.filter(parrent_id = id).all()
        except UserTask.DoesNotExist:
            task = None
            
    if mode == "new":
        owner  = user.id
        task = UserTask(
            owner_id = user.id,
            doer_id = doer,
            cehuch = cehuch,
            date_end = date_end,
            title = title,
            desc = desc,
            task_num = task_num,
            task_date = task_date,
        )
        if parrent != 0:
            task.parrent_id = parrent
        if date_start:
            task.date_start = date_start

    if mode == "edit":
        task.doer_id = doer
        task.cehuch = cehuch
        task.date_end = date_end
        task.title = title
        task.desc = desc
        task.task_num = task_num
        task.task_date = task_date
            
    if task:
        task.save()
        mode = "edit"
        id = task.id
        
        try:
            handle_uploaded_file(id, request.FILES['file'])
        except:
            pass  
    
    if parrent != 0:
        id = parrent
    
    return HttpResponseRedirect("/to/edittask?mode=%s&id=%d" % (mode, id))


@check_login     
@csrf_protect
def file(request, user):
    """Работа с файлом прикрепленным к задаче"""
    id = request.GET.get('id','')
    mode = request.GET.get('mode','')
    name = request.GET.get('name','')
    
    if id != "":
        try:
            task = UserTask.objects.get(pk = id)   
        except UserTask.DoesNotExist:
            task = None
    back_url = "/to/tasks"
    if task and (user.admin or  task.owner_id == user.id):
        back_url = "/to/edittask?mode=%s&id=%d" % ("edit", task.id)
        if mode == "delete":
            dest =  FILE_UPLOAD_DIR + "/%d__%s" % (task.id, name)
            default_storage.delete(dest)

    return HttpResponseRedirect(back_url)
         

    
@check_login     
@csrf_protect
def deltask(request, user):
    """Удаление задачи"""  
    id = request.GET.get('id','')
    
    if id != "":
        try:
            task = UserTask.objects.get(pk = id)   
            subtask = UserTask.objects.filter(parrent_id = id).all()
        except UserTask.DoesNotExist:
            task = None
    back_url = "/to/tasks"
    if task:
        if task.parrent:
            back_url = "/to/edittask?mode=%s&id=%d" % ("edit", task.parrent_id)
        task.delete()
        
    
    return HttpResponseRedirect(back_url)
         
        