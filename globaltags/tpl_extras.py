from datetime import date, datetime, time, timedelta
from django import template
from django.utils.safestring import mark_safe
from django.template import Context

class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def render(self, context):
        context.dicts[0][self.name] = self.value.resolve(context, True)
        return ''

def do_assign(parser, token):
    """
    Assign an expression to a variable in the current context.
    Syntax::
        {% assign [name] [value] %}
    Example::
        {% assign list entry.get_related %}
    """
    
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return AssignNode(bits[1], value)
   
register = template.Library()
register.tag('assign', do_assign)

@register.simple_tag(name='paginator', takes_context=True)
def do_paginator(context, object, name, tab):
    """
    Paginate object.
    
    Syntax::
        {% paginate [object] [name] [tab] %}
    Example::
        {%  %}
        
    """
    if object.paginator.num_pages==1:
        pages = []
    else:
        pages = range(1,object.paginator.num_pages+1)
    
    t = template.loader.get_template('paginator.html')
    return t.render(Context({'items': object, 'pages':pages, 'name':name,'tab':tab}, autoescape=context.autoescape))
    

@register.filter()
def nbsp(value):
    return mark_safe("&nbsp;".join(value.split(' ')))
    
@register.filter
def item(dictionary, key):
    try:
        return dictionary.get(key)
    except:
        return None

@register.filter
def get_key(dictionary, key):
    try:
        return dictionary.keys()[dictionary.values().index(key)]
    except:
        return None
        
@register.filter
def val(object, key):
    return getattr(object, key)

@register.filter
def none(object, key):
    if object == None: 
        return key 
    else:
        return object
      
@register.filter
def addnow(object):
    dt = datetime.combine(date.today(), time(0, 0)) + timedelta(days=object)
    return dt

@register.filter
def to_int(value):
    return int(value)

@register.filter
def minus(value):
    return -1*int(value)    
    
@register.filter
def fio(value):
    fio = value.split(" ") 
    out = "%s %s. %s." % (fio[0] , fio[1][0] , fio[2][0]) 
    
    return out

@register.filter
def banknumbers(value):
    if (value==0):
        return ""
    return '{:,.0f}'.format(value).replace(',', ' ')
    
@register.filter
def age_day(value):
    now = datetime.now()
    try:
        value = value.replace(tzinfo=None)
        difference = now - value
    except:
        return value
    return difference.days

@register.filter
def addstr(object, key):
    s1 = str(object)
    s2 = str(key)
    return s1+s2    

@register.filter
def accessCeh(object, key):
    try: 
        objceh = int(object)
        userceh = int(key)
    except:
        return False
    
    if (userceh % 100 == 0 and userceh/100 == objceh/100) or userceh == objceh:
        return True
    
    return False      

@register.filter
def div(value, arg): 
    return int(value) / int(arg)    

@register.filter
def ceh(value): 
    result = 0
    try:
        result = int(value) / 100 
    except:
        result = value
    return result