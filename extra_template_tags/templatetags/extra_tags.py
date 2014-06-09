from django import template
from django.http import QueryDict
from math import floor

# Permite crear variables en un template --> https://djangosnippets.org/snippets/539/
class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def render(self, context):
        context.dicts[0][self.name]  = self.value.resolve(context, True)
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
#--------------------------------------------------------------------------------------------------
# Borra todas las apariciones de un string
#Example: {{ somevariable|cut:"0" }}
def cut(value, arg):
    "Removes all values of arg from the given string"
    return value.replace(arg, '')

#--------------------------------------------------------------------------------------------------
# Remplaza un caracter por otro
# Example: {{ attr.name|replace:"target=_&replacement= " }}
def replace(value, args):
    qs = QueryDict(args)
    if qs.has_key('target') and qs.has_key('replacement'):
        return value.replace(qs['target'], qs['replacement'])
    else:
        return value
#--------------------------------------------------------------------------------------------------
# Remplaza un caracter por otro
# Example: {{ attr.name|replace:"target=_&replacement= " }}
def clean_str(value):
    value = value.replace(".", "")
    return value.replace("/", "")

#--------------------------------------------------------------------------------------------------
# Convierte un decimal a una hora
# Example: {{ attr.name|decimal_to_time:10.5 }}
def decimal_to_time(value):

    nro = float(value)

    minutes = nro * 60
    hour = int(floor(minutes/60.0))
    minutes = int(minutes - hour * 60.0)
    time = str(minutes)+" min"
    if hour > 0:
        time = str(hour)+" hs "+time

    return time

#--------------------------------------------------------------------------------------------------
# Convierte un decimal a una hora
# Example: {{ attr.name|decimal_to_time:10.5 }}
def date_picker_format(value):

    if value == None:
        return None

    list = value.split("-")

    if len(list) != 3:
        return None

    year = list[0]
    month = list[1]
    day = list[2]

    if int(month) < 10:
        month = "0"+str(int(month))
    if int(day) < 10:
        day = "0"+str(int(day))

    value = year +"-"+ month +"-"+day

    return value

#--------------------------------------------------------------------------------------------------
# Registro los filtros
register = template.Library()
register.tag('assign', do_assign)
register.filter('cut', cut)
register.filter('replace', replace)
register.filter('clean_str', clean_str)
register.filter('decimal_to_time', decimal_to_time)
register.filter('date_picker_format', date_picker_format)