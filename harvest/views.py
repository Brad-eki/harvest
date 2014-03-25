from django.shortcuts import render_to_response
from django.template.context import RequestContext
from harvest.models import Project

# Create your views here.

# Navigation
def home(request):
    return render_to_response('home.html',context_instance=RequestContext(request))

def reports(request):
    return render_to_response('reports.html',context_instance=RequestContext(request))

def timesheet(request):
    return render_to_response('timesheet.html',context_instance=RequestContext(request))

def manage(request):
    return render_to_response('manage.html',context_instance=RequestContext(request))


# Sub-Navigation
def list_project(request):
    projects = Project.objects.all()
    return render_to_response('project_list.html',context_instance=RequestContext(request))

def list_users(request):
    projects = Project.objects.all()
    return render_to_response('users_list.html',context_instance=RequestContext(request))

def list_tasks(request):
    projects = Project.objects.all()
    return render_to_response('tasks_list.html',context_instance=RequestContext(request))
