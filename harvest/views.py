from django.template.context import RequestContext
from django.contrib import auth
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from harvest.models import *
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from harvest.forms import *
from django.db.models import Q
import json
import urllib
from django.core.files import File
from django.core.files.storage import default_storage
from django.db.models import FileField



#-------------------------------------------------------------------------------------------------------------#
#------------------------Helper Methods-----------------------------------------------------------------------#
def userList(request):
    users = None
    if request.method == 'GET' and request.GET.get("search")!=None:
        q = request.GET.get("search")
        users = User.objects.filter(
                    Q(is_active=1),
                    Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)
                )

    else:
        users = User.objects.filter(is_active=1).order_by('username')

    return users


def projectList(request):
    projects = None
    if request.method == 'GET' and request.GET.get("search")!=None:
        q = request.GET.get("search")
        projects = Project.objects.filter(
                    Q(is_active=1),
                    Q(name__icontains=q) | Q(type__icontains=q) | Q(client__icontains=q)
                    )

    else:
        projects = Project.objects.filter(is_active=1).order_by('name')

    return projects

#-------------------------------------------------------------------------------------------------------------#
def user_is_staff(user):
    return user.is_staff

def user_is_not_staff(user):
    return not user.is_staff

# Error
def error_403(request):
    return render_to_response('error/403.html',context_instance=RequestContext(request))

def error_404(request):
    return render_to_response('error/404.html',context_instance=RequestContext(request))

def error_405(request):
    return render_to_response('error/405.html',context_instance=RequestContext(request))

def error_500(request):
    return render_to_response('error/500.html',context_instance=RequestContext(request))

def error_503(request):
    return render_to_response('error/503.html',context_instance=RequestContext(request))
#-------------------------------------------------------------------------------------------------------------#
# Navigation
@login_required
def home(request):
    return render_to_response('home/home.html', {},context_instance=RequestContext(request))
#-------------------------------------------------------------------------------------------------------------#
@login_required
@user_passes_test(user_is_staff,login_url='/error/404',redirect_field_name='')
def reports_user_list(request):
    users = userList(request)
    return render_to_response('reports/user_list.html',{'users':users,"search":request.GET.get("search")},context_instance=RequestContext(request))
#-------------------------------------------------------------------------------------------------------------#
@login_required
@user_passes_test(user_is_staff,login_url='/error/404',redirect_field_name='')
def reports_project_list(request):
    projects = projectList(request)
    return render_to_response('reports/project_list.html',{'projects':projects,"search":request.GET.get("search")},context_instance=RequestContext(request))
#-------------------------------------------------------------------------------------------------------------#
@login_required
def user_report(request,userId):
    return render_to_response('reports/user_report.html',context_instance=RequestContext(request))
#-------------------------------------------------------------------------------------------------------------#
@login_required
@user_passes_test(user_is_staff,login_url='/error/404',redirect_field_name='')
def project_report(request,projectId):
    return render_to_response('reports/project_report.html',context_instance=RequestContext(request))
#-------------------------------------------------------------------------------------------------------------#
@login_required
def timesheet(request):
    return render_to_response('timesheet/timesheet.html',context_instance=RequestContext(request))



#-------------------------------------------------------------------------------------------------------------#
#***************************************** PROJECT VIEWS *********************************************************
#-------------------------------------------------------------------------------------------------------------#
@login_required
@user_passes_test(user_is_staff,login_url='/error/404',redirect_field_name='')
def admin_project_list(request):
    projects = projectList(request)
    return render_to_response('admin/project/project_list.html',{'projects':projects,"search":request.GET.get("search")},context_instance=RequestContext(request))

#-------------------------------------------------------------------------------------------------------------#

@login_required
@user_passes_test(user_is_staff,login_url='/error/404',redirect_field_name='')
def admin_archived_projects(request):
    projects = Project.objects.filter(Q(is_active=0))
    return render_to_response('admin/project/archived_projects.html',{'projects':projects},context_instance=RequestContext(request))


@login_required
@user_passes_test(user_is_staff,login_url='/error/404',redirect_field_name='')
def admin_archive_project(request,projectId):
    if(request.GET  and request.GET.get("archive")):
        #TODO: obtener el id de la url y remplazar
        project = Project.objects.get(id=int(projectId))
        if project:
            if request.GET.get("archive") == "true" or request.GET.get("archive") == "True" or request.GET.get("archive") == "1":
                project.is_active = False
            else:
                project.is_active = True

            project.save()

    return HttpResponse(json.dumps("{}"), content_type = "application/json")


#-------------------------------------------------------------------------------------------------------------#
@login_required
@user_passes_test(user_is_staff,login_url='/error/404',redirect_field_name='')
def admin_create_project(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ProjectForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save();
            return HttpResponseRedirect("/manage/projects")
        else:
            return render_to_response('admin/project/create_project.html',{'form':form},context_instance=RequestContext(request))
    else:
        form = ProjectForm()
        return render_to_response('admin/project/create_project.html',{'form':form},context_instance=RequestContext(request))

#-------------------------------------------------------------------------------------------------------------#
@login_required
@user_passes_test(user_is_staff,login_url='/error/404',redirect_field_name='')
def edit_project(request,projectId):

    projects = Project.objects.filter(id=projectId)
    project = projects[0]
    projectUsers = User.objects.filter(Q(projects__in=projects), Q(is_active=1))
    users = User.objects.filter(is_active=1)

    if request.POST.get("submenu") == "project_profile":
        form = ProjectForm(request.POST)
        if form.is_valid(): # All validation rules pass
            form.save()
            return render_to_response('admin/project/edit_project.html',{'form':form,'projectUsers':projectUsers,'users':users,'profileChangedSuccesful':1,'submenu':request.POST.get('submenu')},context_instance=RequestContext(request))
        else:
            return render_to_response('admin/project/edit_project.html',{'form':form,'projectUsers':projectUsers,'users':users,'profileChangedSuccesful':0,'submenu':request.POST.get('submenu')},context_instance=RequestContext(request))

    else:
        form = ProjectForm(initial={'id':project.id, 'name':project.name, 'client':project.client, 'type':project.type,'estimated_hours':project.estimated_hours})
        return render_to_response('admin/project/edit_project.html',{'form':form,'projectUsers':projectUsers,'users':users},context_instance=RequestContext(request))


@login_required
@user_passes_test(user_is_staff,login_url='/error/404',redirect_field_name='')
def admin_remove_user_from_project(request,projectId,userId):
    if request.method == "DELETE":
        project = Project.objects.get(id=projectId)
        user = User.objects.get(id=userId)
        user.projects.remove(project)
        print "user_id: "+userId
        print "project_id: "+projectId

    return HttpResponse(json.dumps("{}"), content_type = "application/json")


@login_required
@user_passes_test(user_is_staff,login_url='/error/404',redirect_field_name='')
def admin_add_users_to_project(request,projectId):
    if request.POST:

        users = request.POST.get("users").split(",")
        if projectId and users and len(users) > 0 :
            project = Project.objects.get(id=projectId)
            if project:
                for userId in users:
                    user = User.objects.get(id=userId)
                    project.users.add(user)

    return HttpResponse(json.dumps("{}"), content_type = "application/json")

#-------------------------------------------------------------------------------------------------------------#
#***************************************** USER VIEWS *********************************************************
#-------------------------------------------------------------------------------------------------------------#
@login_required
@user_passes_test(user_is_staff,login_url='/error/404',redirect_field_name='')

def admin_create_user(request):
    if request.method == 'POST': # If the form has been submitted...
        form = UserForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save();
            return HttpResponseRedirect("/manage/users")
        else:
            return render_to_response('admin/user/create_user.html',{'form':form},context_instance=RequestContext(request))
    else:
        form = UserForm()
        return render_to_response('admin/user/create_user.html',{'form':form},context_instance=RequestContext(request))

#-------------------------------------------------------------------------------------------------------------#

@login_required
@user_passes_test(user_is_staff,login_url='/error/404',redirect_field_name='')
def edit_user_profile(request,userId):

    users = User.objects.filter(id=userId)
    user = users[0]
    userProjects = Project.objects.filter(Q(users__in=users), Q(is_active=1))
    projects = Project.objects.filter(is_active=1)

    if request.POST and request.POST.get("submenu") == "profile_password":
        form = EditUserPasswordForm(request.POST)
        successful = 1
        if form.is_valid(): # All validation rules pass
            form.save()
        else:
            successful = 0

        user = User.objects.get(id=userId)
        form = EditUserForm(initial={'id':user.id, 'username':user.username, 'first_name':user.first_name,'last_name':user.last_name,'email':user.email,'is_staff':user.is_staff,'thumbnail':user.thumbnail})
        return render_to_response('admin/user/edit_profile.html',{'form':form,'userProjects':userProjects,'projects':projects},context_instance=RequestContext(request))

    elif request.POST:
        print str(request.POST)
        form = EditUserForm(request.POST, request.FILES)
        if form.is_valid(): # All validation rules pass
            user = form.save()
            form.initial = {'thumbnail':user.thumbnail}
            return render_to_response('admin/user/edit_profile.html',{'form':form,'userProjects':userProjects,'projects':projects,'profileChangedSuccesful':1,'submenu':request.POST.get('submenu')},context_instance=RequestContext(request))
        else:
            print form.errors
            user = User.objects.get(id=userId)
            form.initial = {'thumbnail':user.thumbnail}
            return render_to_response('admin/user/edit_profile.html',{'form':form,'userProjects':userProjects,'projects':projects,'error':form.errors,'profileChangedSuccesful':0,'submenu':request.POST.get('submenu')},context_instance=RequestContext(request))

    else:
        form = EditUserForm(initial={'id':user.id, 'username':user.username, 'first_name':user.first_name,'last_name':user.last_name,'email':user.email,'is_staff':user.is_staff,'thumbnail':user.thumbnail})
        return render_to_response('admin/user/edit_profile.html',{'form':form,'userProjects':userProjects,'projects':projects},context_instance=RequestContext(request))

#-------------------------------------------------------------------------------------------------------------#
@login_required
@user_passes_test(user_is_staff,login_url='/error/404',redirect_field_name='')
def admin_remove_project_from_user(request,userId,projectId):
    if request.method == "DELETE":
        user = User.objects.get(id=userId)
        project = Project.objects.get(id=projectId)
        project.users.remove(user)

        print "user_id: "+userId
        print "project_id: "+projectId

    return HttpResponse(json.dumps("{}"), content_type = "application/json")
#-------------------------------------------------------------------------------------------------------------#
@login_required
@user_passes_test(user_is_staff,login_url='/error/404',redirect_field_name='')
def admin_add_projects_to_user(request,userId):
    if request.POST:
        projects = request.POST.get("projects").split(",")
        if userId and projects and len(projects) > 0 :
            user = User.objects.get(id=userId)
            if user:
                for projectId in projects:
                    project = Project.objects.get(id=projectId)
                    user.projects.add(project)

    return HttpResponse(json.dumps("{}"), content_type = "application/json")
#-------------------------------------------------------------------------------------------------------------#

@login_required
@user_passes_test(user_is_staff,login_url='/error/404',redirect_field_name='')
def admin_archived_users(request):
    users = User.objects.filter(Q(is_active=0))
    return render_to_response('admin/user/archived_users.html',{'users':users},context_instance=RequestContext(request))


@login_required
@user_passes_test(user_is_staff,login_url='/error/404',redirect_field_name='')
def admin_archive_user(request, userId):
    if(request.GET  and request.GET.get("archive")):
        #TODO: obtener el id de la url y remplazar
        user = User.objects.get(id=int(userId))
        if user:
            if request.GET.get("archive") == "true" or request.GET.get("archive") == "True" or request.GET.get("archive") == "1":
                user.is_active = False
            else:
                user.is_active = True
            user.save()

    return HttpResponse(json.dumps("{}"), content_type = "application/json")

#-------------------------------------------------------------------------------------------------------------#

@login_required
@user_passes_test(user_is_staff,login_url='/error/404',redirect_field_name='')
def admin_user_list(request):
    users = userList(request)
    return render_to_response('admin/user/user_list.html',{'users':users,"search":request.GET.get("search")},context_instance=RequestContext(request))

#-------------------------------------------------------------------------------------------------------------#
def login(request):

    next = ""
    if request.GET:
        next = request.GET.get('next', '')

    if not next and request.POST:
        next = request.POST.get('next', '')

    print "NEXT --> "+next

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                user = auth.authenticate(username=user.username, password=password)
            else:
                user = auth.authenticate(username=username, password=password)

        except User.DoesNotExist:
            user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            if not next:
                next = settings.LOGIN_REDIRECT_URL
            return HttpResponseRedirect(next)
        else:
            # Show an error page
            if not next:
                return render_to_response('admin/user/login.html',{'error': True,},context_instance=RequestContext(request))
            else:
                return render_to_response('admin/user/login.html',{'next':next,'error': True,},context_instance=RequestContext(request))
    else:
        if not next:
            return render_to_response('admin/user/login.html',context_instance=RequestContext(request))
        else:
            return render_to_response('admin/user/login.html',{'next':next,},context_instance=RequestContext(request))
#---------------------------------------------------------------------------------#
