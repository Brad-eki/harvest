from django.shortcuts import render_to_response
from django.template.context import RequestContext
from harvest.models import Project

# Create your views here.

# Navigation
def home(request):
    return render_to_response('home/home.html', {},context_instance=RequestContext(request))


def reports_user_list(request):
    return render_to_response('reports/user_list.html',context_instance=RequestContext(request))

def reports_project_list(request):
    return render_to_response('reports/project_list.html',context_instance=RequestContext(request))

def user_report(request):
    return render_to_response('reports/user_report.html',context_instance=RequestContext(request))

def project_report(request):
    return render_to_response('reports/project_report.html',context_instance=RequestContext(request))


def timesheet(request):
    return render_to_response('timesheet/timesheet.html',context_instance=RequestContext(request))


def admin_user_list(request):
    return render_to_response('admin/user/user_list.html',context_instance=RequestContext(request))

def admin_project_list(request):
    return render_to_response('admin/project/project_list.html',context_instance=RequestContext(request))

def admin_user(request):
    return render_to_response('admin/user/user.html',context_instance=RequestContext(request))

def admin_archived_users(request):
    return render_to_response('admin/user/archived_users.html',context_instance=RequestContext(request))

def admin_archived_projects(request):
    return render_to_response('admin/project/archived_projects.html',context_instance=RequestContext(request))

def edit_project(request):
    return render_to_response('admin/project/edit_project.html',context_instance=RequestContext(request))

def admin_create_user(request):
    return render_to_response('admin/user/create_user.html',context_instance=RequestContext(request))

def admin_create_project(request):
    return render_to_response('admin/project/create_project.html',context_instance=RequestContext(request))

def login(request):
    return render_to_response('admin/user/login.html',context_instance=RequestContext(request))

def edit_user_profile(request):
    return render_to_response('admin/user/edit_profile.html',context_instance=RequestContext(request))