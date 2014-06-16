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
import time
from datetime import timedelta, datetime, time
from django.utils.timezone import localtime
from django.utils import timezone
from django.db.models import Sum
import array

#-------------------------------------------------------------------------------------------------------------#
#------------------------Helper Methods-----------------------------------------------------------------------#
def last_report(user):
    tasks = Task.objects.filter(user=user).order_by('-modified')
    if tasks:
        return tasks[0].date
        #.strftime('%d %b %Y')
    else:
        return None

def userList(request):
    users = None

    if request.method == 'GET' and request.GET.get("search") != None:
        q = request.GET.get("search")
        users = User.objects.filter(
            Q(is_active=1),
            Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)
        )
    else:
        users = User.objects.filter(is_active=1).order_by('username')

    for user in users:
        user.last_report = last_report(user)

    return users


def projectList(request):
    projects = None
    if request.method == 'GET' and request.GET.get("search") != None:
        q = request.GET.get("search")

        if request.user.is_staff:
            print "staff"
            projects = Project.objects.filter(
                Q(is_active=1),
                Q(name__icontains=q) | Q(type__icontains=q) | Q(client__icontains=q)
            ).order_by('name')
        else:
            projects = Project.objects.filter(
                Q(is_active=1),
                Q(users__in=[request.user]),
                Q(name__icontains=q) | Q(type__icontains=q) | Q(client__icontains=q)
            ).order_by('name')

    else:
        if request.user.is_staff:
            projects = Project.objects.filter(is_active=1).order_by('name')
        else:
            projects = Project.objects.filter(
                Q(is_active=1),
                Q(users__in=[request.user]),
            ).order_by('name')

    return projects

#-------------------------------------------------------------------------------------------------------------#
def user_is_staff(user):
    return user.is_staff


def user_is_not_staff(user):
    return not user.is_staff


def is_staff_or_current_user(user, userId):
    if user.is_staff:
        return True

    if user.id != int(userId):
        return False

    return True


#-------------------------------------------------------------------------------------------------------------#

# Error
def error_400(request):
    return render_to_response('error/400.html', context_instance=RequestContext(request))


def error_403(request):
    return render_to_response('error/403.html', context_instance=RequestContext(request))


def error_404(request):
    return render_to_response('error/404.html', context_instance=RequestContext(request))


def error_405(request):
    return render_to_response('error/405.html', context_instance=RequestContext(request))


def error_500(request):
    return render_to_response('error/500.html', context_instance=RequestContext(request))


def error_503(request):
    return render_to_response('error/503.html', context_instance=RequestContext(request))


#-------------------------------------------------------------------------------------------------------------#
@login_required
def task(request, taskId=None):
    if request.method == 'DELETE':
        task = Task.objects.get(id=taskId)
        if task:
            task.delete()
            return HttpResponse(json.dumps("{}"), content_type="application/json")
        else:
            return HttpResponse(json.dumps("{'error':'task not exist'}"), content_type="application/json")
    else:

        if request.method == 'POST':  # If the form has been submitted...
            form = TaskForm(request.user,request.POST)  # A form bound to the POST data

        if form.is_valid():  # All validation rules pass
            task = form.save();
            return HttpResponse(json.dumps({"taskId":str(task.id)}), content_type="application/json")
        else:
            print form.errors
            return HttpResponse(json.dumps("{'error':'unexpected error'}"), content_type="application/json")


#-------------------------------------------------------------------------------------------------------------#
# Navigation
@login_required
def home(request):
    today = 0
    week = 0
    month = 0
    year = 0
    allMonths = [{'name': 'January', 'hours': 0}, {'name': 'February', 'hours': 0}, {'name': 'March', 'hours': 0},
                 {'name': 'April', 'hours': 0}, {'name': 'May', 'hours': 0}, {'name': 'June', 'hours': 0},
                 {'name': 'July', 'hours': 0}, {'name': 'August', 'hours': 0}, {'name': 'September', 'hours': 0},
                 {'name': 'October', 'hours': 0}, {'name': 'November', 'hours': 0}, {'name': 'December', 'hours': 0}];

    some_day_last_week = timezone.now().date() - timedelta(days=7)
    monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + timedelta(days=7)

    now = datetime.now().replace(microsecond=0)

    today = Task.objects.filter(user=request.user).filter(date=now.date()).aggregate(Sum('duration'))[
        "duration__sum"]
    if not today:
        today = '0'

    week = Task.objects.filter(user=request.user).filter(date__range=[monday_of_this_week, now.date()]).aggregate(
        Sum('duration'))["duration__sum"]
    if not week:
        week = '0'

    month = Task.objects.filter(user=request.user).filter(date__month=6).aggregate(Sum('duration'))["duration__sum"]

    if not month:
        month = '0'

    year = Task.objects.filter(user=request.user).filter(date__year=now.year).aggregate(Sum('duration'))[
        "duration__sum"]
    if not year:
        year = '0'

    i = 1
    for aMonth in allMonths:
        hours = Task.objects.filter(user=request.user).filter(date__month=i).aggregate(Sum('duration'))[
            "duration__sum"]
        i += 1
        if not hours:
            hours = '0'
        aMonth['hours'] = hours

    return render_to_response('home/home.html',
                              {'today': today, 'week': week, 'month': month, 'year': year, 'allMonths': allMonths},
                              context_instance=RequestContext(request))


#-------------------------------------------------------------------------------------------------------------#
@login_required
@user_passes_test(user_is_staff, login_url='/error/404', redirect_field_name='')
def reports_user_list(request):
    users = userList(request)
    return render_to_response('reports/user_list.html', {'users': users, "search": request.GET.get("search")},
                              context_instance=RequestContext(request))


#-------------------------------------------------------------------------------------------------------------#
@login_required
def reports_project_list(request):
    projects = projectList(request)
    return render_to_response('reports/project_list.html', {'projects': projects, "search": request.GET.get("search")},
                              context_instance=RequestContext(request))


#-------------------------------------------------------------------------------------------------------------#
@login_required
def user_report(request, userId):
    if not is_staff_or_current_user(request.user, userId):
        return HttpResponseRedirect("/reports/users/" + str(request.user.id) + "/")

    now = datetime.now()
    lastWeek = now - timedelta(days=7)
    fromStrDate = None
    toStrDate = None
    selectedProjects = []
    anUser = User.objects.get(id=userId)
    users = [anUser]

    if request.GET.get("from"):
        fromStrDate = request.GET.get("from")
    else:
        fromStrDate = str(lastWeek.year) + "-" + str(lastWeek.month) + "-" + str(lastWeek.day)

    if request.GET.get("to"):
        toStrDate = request.GET.get("to")
    else:
        toStrDate = str(now.year) + "-" + str(now.month) + "-" + str(now.day)

    if request.GET.get("projects"):
        selectedProjects = request.GET.getlist("projects")
    else:
        tasks = Task.objects.filter(user=anUser).order_by('-modified')
        if tasks:
            selectedProjects = [str(tasks[0].project.id)]
        else:
            projects = Project.objects.filter(Q(users__in=users)).order_by("-created")
            if projects:
                selectedProjects = [projects[0].id]

    projects = Project.objects.filter(Q(users__in=users), Q(is_active=1))
    fromDate = datetime.strptime(fromStrDate, "%Y-%m-%d").date()
    toDate = datetime.strptime(toStrDate, "%Y-%m-%d").date()

    tasks = None
    total = 0.0
    print selectedProjects
    if selectedProjects:
        tasks = Task.objects.filter(Q(user=anUser, project__in=selectedProjects)).filter(
            date__range=(fromDate, toDate))
        print tasks
        for task in tasks:
            total += float(task.duration)

    print selectedProjects
    return render_to_response('reports/user_report.html',
                              {'tasks': tasks, "total": total, 'projects': projects, 'to': toStrDate, 'from': fromStrDate,
                               'selectedProjects': selectedProjects}, context_instance=RequestContext(request))


#-------------------------------------------------------------------------------------------------------------#
@login_required
def project_report(request, projectId):
    project = Project.objects.get(id=projectId)
    users = User.objects.filter(projects__in=[project])
    fromStrDate = None
    toStrDate = None
    now = datetime.now()

    if request.GET.get("from"):
        fromStrDate = request.GET.get("from")
    else:
        created = project.created
        fromStrDate = str(created.year) + "-" + str(created.month) + "-" + str(created.day)

    if request.GET.get("to"):
        toStrDate = request.GET.get("to")
    else:
        toStrDate = str(now.year) + "-" + str(now.month) + "-" + str(now.day)

    typeNames = []
    rows = []
    i = 0
    j = 0

    totalRow = []
    for value in Task.TASK_TYPE:
        typeNames.insert(i, value[0])
        totalRow.insert(i, 0)
        i += 1

    totalRow.insert(i, 0)  #Total
    lastIndex = len(totalRow) - 1
    fromDate = datetime.strptime(fromStrDate, "%Y-%m-%d").date()
    toDate = datetime.strptime(toStrDate, "%Y-%m-%d").date()

    for aUser in users:
        row = []
        name = ""

        if aUser.first_name == "":
            name = aUser.username
        else:
            name = aUser.first_name + " " + aUser.last_name

        row.insert(0, name)

        i = 1
        total = 0
        for type in typeNames:
            hours = Task.objects.filter(user=aUser, project=project, type=type).filter(
               date__range=(fromDate, toDate)).aggregate(Sum('duration'))["duration__sum"]
            if hours == None:
                hours = 0
            row.insert(i, hours)
            total += hours
            totalRow[i - 1] = totalRow[i - 1] + hours
            totalRow[lastIndex] = totalRow[lastIndex] + hours
            i += 1

        row.insert(i, total)
        rows.insert(j, row)
        j += 1

    total = totalRow[lastIndex]
    taskChart = []
    userChart = []

    if total != 0:
        colors = ['#68BC31', '#2091CF', '#AF4E96', '#DA5430', '#FEE074', '#a069c3', '#f79263', '#6fb3e0', '#f89406',
                  '#5bc0de', '#85144b', '#0073b7', '#fcf8e3', '#B94A48']

        i = 0
        for type in typeNames:
            if i < len(colors):
                color = colors[i]
            else:
                color = colors[int(i / len(colors))]

            percentage = round((totalRow[i] / total) * 100, 2)
            taskChart.insert(i, {'name': type, 'percentage': percentage, 'color': color})
            i += 1


        i = 0
        for row in rows:
            if i < len(colors):
                color = colors[i]
            else:
                color = colors[int(i / len(colors))]

            percentage = round((row[len(row) - 1] / total) * 100, 2)
            userChart.insert(i, {'name': row[0], 'percentage': percentage, 'color': color})
            i += 1

    return render_to_response('reports/project_report.html',
                              {'projectName': project.name, 'projectType': project.type, 'typeNames': typeNames,
                               'rows': rows, 'totalRow': totalRow, 'to': toStrDate, 'from': fromStrDate,
                               'taskChart': taskChart, 'userChart': userChart},
                              context_instance=RequestContext(request))


#-------------------------------------------------------------------------------------------------------------#
@login_required
def timesheet(request, year='0', month='0', day='0'):
    try:
        strDate = year + "/" + month + "/" + day
        currentDay = datetime.strptime(strDate, "%Y/%m/%d").date()
    except:
        currentDay = datetime.now().date()

    some_day_last_week = currentDay - timedelta(days=7)
    monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))

    days = []
    titles = ['M', 'T', 'W', 'Th', 'F', 'S', 'Su']
    totalHours = 0
    for i in range(0, 7):
        date = monday_of_last_week + timedelta(days=7 + i)
        taskHours = Task.objects.filter(user=request.user, date=date).aggregate(Sum('duration'))["duration__sum"]
        if not taskHours:
            taskHours = '0.00'
        else:
            totalHours += taskHours
        days.insert(i, {'title': titles[i], 'date': date, 'hours': taskHours})

    today = timezone.now().date()
    nextDay = currentDay - timedelta(days=1)
    previousDay = currentDay - timedelta(days=-1)


    tasks = Task.objects.filter(user=request.user, date=currentDay).order_by("modified")

    userProjects = Project.objects.filter(Q(users__in=[request.user]), Q(is_active=1))

    return render_to_response('timesheet/timesheet.html',
                              {'projects': userProjects, 'tasksTypes': Task.TASK_TYPE, 'today': today,
                               'nextDay': nextDay, 'previousDay': previousDay, 'days': days, 'currentDay': currentDay,
                               'totalHours': totalHours, 'tasks': tasks}, context_instance=RequestContext(request))


#-------------------------------------------------------------------------------------------------------------#
#***************************************** PROJECT VIEWS *********************************************************
#-------------------------------------------------------------------------------------------------------------#
@login_required
@user_passes_test(user_is_staff, login_url='/error/404', redirect_field_name='')
def admin_project_list(request):
    projects = projectList(request)
    return render_to_response('admin/project/project_list.html',
                              {'projects': projects, "search": request.GET.get("search")},
                              context_instance=RequestContext(request))


#-------------------------------------------------------------------------------------------------------------#

@login_required
@user_passes_test(user_is_staff, login_url='/error/404', redirect_field_name='')
def admin_archived_projects(request):
    projects = Project.objects.filter(Q(is_active=0))
    return render_to_response('admin/project/archived_projects.html', {'projects': projects},
                              context_instance=RequestContext(request))


@login_required
@user_passes_test(user_is_staff, login_url='/error/404', redirect_field_name='')
def admin_archive_project(request, projectId):
    if (request.GET and request.GET.get("archive")):
        project = Project.objects.get(id=int(projectId))
        if project:
            if request.GET.get("archive") == "true" or request.GET.get("archive") == "True" or request.GET.get(
                    "archive") == "1":
                project.is_active = False
            else:
                project.is_active = True

            project.save()

    return HttpResponse(json.dumps("{}"), content_type="application/json")


#-------------------------------------------------------------------------------------------------------------#
@login_required
@user_passes_test(user_is_staff, login_url='/error/404', redirect_field_name='')
def admin_create_project(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = ProjectForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            form.save();
            return HttpResponseRedirect("/manage/projects")
        else:
            return render_to_response('admin/project/create_project.html', {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = ProjectForm()
        return render_to_response('admin/project/create_project.html', {'form': form},
                                  context_instance=RequestContext(request))


#-------------------------------------------------------------------------------------------------------------#
@login_required
@user_passes_test(user_is_staff, login_url='/error/404', redirect_field_name='')
def edit_project(request, projectId):
    projects = Project.objects.filter(id=projectId)
    project = projects[0]
    projectUsers = User.objects.filter(Q(projects__in=projects), Q(is_active=1))
    users = User.objects.filter(is_active=1)

    if request.POST.get("submenu") == "project_profile":
        form = ProjectForm(request.POST)
        if form.is_valid():  # All validation rules pass
            form.save()
            return render_to_response('admin/project/edit_project.html',
                                      {'form': form, 'projectUsers': projectUsers, 'users': users,
                                       'profileChangedSuccesful': 1, 'submenu': request.POST.get('submenu')},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('admin/project/edit_project.html',
                                      {'form': form, 'projectUsers': projectUsers, 'users': users,
                                       'profileChangedSuccesful': 0, 'submenu': request.POST.get('submenu')},
                                      context_instance=RequestContext(request))

    else:
        form = ProjectForm(
            initial={'id': project.id, 'name': project.name, 'client': project.client, 'type': project.type,
                     'estimated_hours': project.estimated_hours})
        return render_to_response('admin/project/edit_project.html',
                                  {'form': form, 'projectUsers': projectUsers, 'users': users},
                                  context_instance=RequestContext(request))


@login_required
@user_passes_test(user_is_staff, login_url='/error/404', redirect_field_name='')
def admin_remove_user_from_project(request, projectId, userId):
    if request.method == "DELETE":
        project = Project.objects.get(id=projectId)
        user = User.objects.get(id=userId)
        user.projects.remove(project)
        print "user_id: " + userId
        print "project_id: " + projectId

    return HttpResponse(json.dumps("{}"), content_type="application/json")


@login_required
@user_passes_test(user_is_staff, login_url='/error/404', redirect_field_name='')
def admin_add_users_to_project(request, projectId):
    if request.POST:

        users = request.POST.get("users").split(",")
        if projectId and users and len(users) > 0:
            project = Project.objects.get(id=projectId)
            if project:
                for userId in users:
                    user = User.objects.get(id=userId)
                    project.users.add(user)

    return HttpResponse(json.dumps("{}"), content_type="application/json")


#-------------------------------------------------------------------------------------------------------------#
#***************************************** USER VIEWS *********************************************************
#-------------------------------------------------------------------------------------------------------------#
@login_required
@user_passes_test(user_is_staff, login_url='/error/404', redirect_field_name='')
def admin_create_user(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = UserForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            form.save();
            return HttpResponseRedirect("/manage/users")
        else:
            return render_to_response('admin/user/create_user.html', {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = UserForm()
        return render_to_response('admin/user/create_user.html', {'form': form},
                                  context_instance=RequestContext(request))


#-------------------------------------------------------------------------------------------------------------#

@login_required
#@user_passes_test(user_is_staff,login_url='/error/404',redirect_field_name='')
def edit_user_profile(request, userId):
    if not is_staff_or_current_user(request.user, userId):
        return HttpResponseRedirect("/manage/users/" + str(request.user.id) + "/edit/")

    users = User.objects.filter(id=userId)
    user = users[0]
    userProjects = Project.objects.filter(Q(users__in=users), Q(is_active=1))
    projects = Project.objects.filter(is_active=1)

    if request.POST and request.POST.get("submenu") == "profile_password":
        form = EditUserPasswordForm(request.POST)
        successful = 1
        if form.is_valid():  # All validation rules pass
            form.save()
        else:
            successful = 0

        user = User.objects.get(id=userId)
        form = EditUserForm(initial={'id': user.id, 'username': user.username, 'first_name': user.first_name,
                                     'last_name': user.last_name, 'email': user.email, 'is_staff': user.is_staff,
                                     'thumbnail': user.thumbnail})
        return render_to_response('admin/user/edit_profile.html',
                                  {'form': form, 'userProjects': userProjects, 'projects': projects, 'passwordChangedSuccesful': 1, 'submenu': request.POST.get('submenu')},
                                  context_instance=RequestContext(request))

    elif request.POST:
        print str(request.POST)
        form = EditUserForm(request.POST, request.FILES)
        if form.is_valid():  # All validation rules pass
            user = form.save()
            form.initial = {'thumbnail': user.thumbnail}
            return render_to_response('admin/user/edit_profile.html',
                                      {'form': form, 'userProjects': userProjects, 'projects': projects,
                                       'profileChangedSuccesful': 1, 'submenu': request.POST.get('submenu')},
                                      context_instance=RequestContext(request))
        else:
            print form.errors
            user = User.objects.get(id=userId)
            form.initial = {'thumbnail': user.thumbnail}
            return render_to_response('admin/user/edit_profile.html',
                                      {'form': form, 'userProjects': userProjects, 'projects': projects,
                                       'error': form.errors, 'profileChangedSuccesful': 0,
                                       'submenu': request.POST.get('submenu')},
                                      context_instance=RequestContext(request))

    else:
        form = EditUserForm(initial={'id': user.id, 'username': user.username, 'first_name': user.first_name,
                                     'last_name': user.last_name, 'email': user.email, 'is_staff': user.is_staff,
                                     'thumbnail': user.thumbnail})
        return render_to_response('admin/user/edit_profile.html',
                                  {'form': form, 'userProjects': userProjects, 'projects': projects},
                                  context_instance=RequestContext(request))


#-------------------------------------------------------------------------------------------------------------#
@login_required
@user_passes_test(user_is_staff, login_url='/error/404', redirect_field_name='')
def admin_remove_project_from_user(request, userId, projectId):
    if request.method == "DELETE":
        user = User.objects.get(id=userId)
        project = Project.objects.get(id=projectId)
        project.users.remove(user)

        print "user_id: " + userId
        print "project_id: " + projectId

    return HttpResponse(json.dumps("{}"), content_type="application/json")


#-------------------------------------------------------------------------------------------------------------#
@login_required
@user_passes_test(user_is_staff, login_url='/error/404', redirect_field_name='')
def admin_add_projects_to_user(request, userId):
    if request.POST:
        projects = request.POST.get("projects").split(",")
        if userId and projects and len(projects) > 0:
            user = User.objects.get(id=userId)
            if user:
                for projectId in projects:
                    project = Project.objects.get(id=projectId)
                    user.projects.add(project)

    return HttpResponse(json.dumps("{}"), content_type="application/json")


#-------------------------------------------------------------------------------------------------------------#

@login_required
@user_passes_test(user_is_staff, login_url='/error/404', redirect_field_name='')
def admin_archived_users(request):
    users = User.objects.filter(Q(is_active=0))
    return render_to_response('admin/user/archived_users.html', {'users': users},
                              context_instance=RequestContext(request))


@login_required
@user_passes_test(user_is_staff, login_url='/error/404', redirect_field_name='')
def admin_archive_user(request, userId):
    if (request.GET and request.GET.get("archive")):
        #TODO: obtener el id de la url y remplazar
        user = User.objects.get(id=int(userId))
        if user:
            if request.GET.get("archive") == "true" or request.GET.get("archive") == "True" or request.GET.get(
                    "archive") == "1":
                user.is_active = False
            else:
                user.is_active = True
            user.save()

    return HttpResponse(json.dumps("{}"), content_type="application/json")


#-------------------------------------------------------------------------------------------------------------#

@login_required
@user_passes_test(user_is_staff, login_url='/error/404', redirect_field_name='')
def admin_user_list(request):
    users = userList(request)
    return render_to_response('admin/user/user_list.html', {'users': users, "search": request.GET.get("search")},
                              context_instance=RequestContext(request))


#-------------------------------------------------------------------------------------------------------------#
def login(request):
    next = ""
    if request.GET:
        next = request.GET.get('next', '')

    if not next and request.POST:
        next = request.POST.get('next', '')

    print "NEXT --> " + next

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
                return render_to_response('admin/user/login.html', {'error': True, },
                                          context_instance=RequestContext(request))
            else:
                return render_to_response('admin/user/login.html', {'next': next, 'error': True, },
                                          context_instance=RequestContext(request))
    else:
        if not next:
            return render_to_response('admin/user/login.html', context_instance=RequestContext(request))
        else:
            return render_to_response('admin/user/login.html', {'next': next, },
                                      context_instance=RequestContext(request))

#---------------------------------------------------------------------------------#
