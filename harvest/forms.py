#encoding:utf-8
from django.forms import  ModelForm
from django import forms
from harvest.models import *
from timesheet import settings
from django.contrib.auth.models import User
from django.core import validators
from django.contrib.auth.hashers import make_password
from django.core.files import File
from datetime import timedelta, datetime, time
import math

#------------------------------------------------------------------------------------------------------------#

def validateUsername(field_data):
    try:
        User.objects.get(username=field_data)
    except User.DoesNotExist:
        return field_data
    raise validators.ValidationError('The username "%s" is already taken.' % field_data)

def validateEmail(field_data):
    try:
        User.objects.get(email=field_data)
    except User.DoesNotExist:
        return field_data
    raise validators.ValidationError('The email "%s" is already taken.' % field_data)

def localAvatarFile(photoId):
    image_name = "avatar" + photoId + ".png"
    image_path = settings.STATIC_AVATAR_ROOT + image_name

    obj = open(image_path)
    if obj:
        file = File(obj)
        return file
    else:
        return None

def nameOfUserAvatar(userId):
    return "avatar_"+userId+".png"


def setFormatToTime(time):
    if not time:
        return None

    array = time.split(":")
    if len(array) == 2:
        min = int(array[1])
        min = (min / 60)
        return array[0]+str(min)

#------------------------------------------------------------------------------------------------------------#
class UserForm(forms.Form):
    username = forms.CharField(max_length=30,min_length=4,required=True,error_messages={'required': 'Please enter your username'},validators=[validateUsername])
    first_name = forms.CharField(max_length=30,required=False)
    last_name = forms.CharField(max_length=30,required=False)
    email = forms.EmailField(max_length=75,required=True,error_messages={'required': 'Please enter a valid email'},validators=[validateEmail])
    password = forms.CharField(max_length=128,min_length=4,required=True)
    confirm_password = forms.CharField(max_length=128,min_length=4,required=True)
    is_staff = forms.BooleanField(required=False);

    def clean_confirm_password(self):

        if (self.cleaned_data.get('password')==None or self.cleaned_data.get('confirm_password')==None):
            return False

        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if (password==confirm_password):
            return True
        else:
            raise validators.ValidationError('The password must match')

    def save(self):
        print "save"
        user = User()
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.password = make_password(self.cleaned_data['password'])
        user.is_staff = self.cleaned_data['is_staff']
        user.is_active = True
        user.save()
        # Assign default thumbnail
        thumbnail_name = nameOfUserAvatar(str(user.id))
        file = localAvatarFile('01')
        if file:
            user.thumbnail.save(thumbnail_name,file , save=True)

        return user


#------------------------------------------------------------------------------------------------------------#
class EditUserForm(forms.Form):
    id = forms.IntegerField(required=True)
    username = forms.CharField(max_length=30,min_length=4,required=True,error_messages={'required': 'Please enter your username'})
    first_name = forms.CharField(max_length=30,required=False)
    last_name = forms.CharField(max_length=30,required=False)
    email = forms.EmailField(max_length=75,required=True,error_messages={'required': 'Please enter a valid email'})
    is_staff = forms.BooleanField(required=False);
    thumbnail = forms.ImageField(required=False)
    photoId = forms.CharField(max_length=255,required=False)

    def clean_username(self):
        userId = self.cleaned_data.get('id')
        user = User.objects.get(id=userId)

        if user and user.username == self.cleaned_data.get('username'):
            return user.username

        return validateUsername(self.cleaned_data.get('username'));

    def clean_email(self):
        userId = self.cleaned_data.get('id')
        user = User.objects.get(id=userId)

        if user and user.email == self.cleaned_data.get('email'):
            return self.cleaned_data.get('email')

        return validateEmail(self.cleaned_data.get('email'));


    def save(self):
        user = User.objects.get(id=self.cleaned_data['id'])
        if user:
            user.username = self.cleaned_data['username']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.is_staff = self.cleaned_data['is_staff']
            user.save()

            if self.cleaned_data['thumbnail']:
                thumbnail_name = self.cleaned_data['thumbnail'].name
                string = thumbnail_name.split('/')[-1]
                format = string.split('.')[-1]
                thumbnail_name = "avatar_"+str(user.id)+"."+format
                user.thumbnail.save(thumbnail_name, self.cleaned_data['thumbnail'], save=True)
            elif self.cleaned_data['photoId']:
                thumbnail_name = nameOfUserAvatar(str(user.id))
                file = localAvatarFile(self.cleaned_data['photoId'])
                if file:
                    user.thumbnail.save(thumbnail_name,file , save=True)


            return user
        else:
            raise validators.ValidationError('Error')


#------------------------------------------------------------------------------------------------------------#
class EditUserPasswordForm(forms.Form):
    id = forms.IntegerField(required=True)
    password = forms.CharField(max_length=128,min_length=4,required=True)
    confirm_password = forms.CharField(max_length=128,min_length=4,required=True)

    def clean_confirm_password(self):

        if (self.cleaned_data.get('password')==None or self.cleaned_data.get('confirm_password')==None):
            return False

        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if (password==confirm_password):
            return True
        else:
            raise validators.ValidationError('The password must match')

    def save(self):
        user = User.objects.get(id=self.cleaned_data['id'])
        if user:
            user.password = make_password(self.cleaned_data['password'])
            user.save()
            return user
        else:
            raise validators.ValidationError('Error')

#------------------------------------------------------------------------------------------------------------#
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'client', 'type','estimated_hours')

    id = forms.IntegerField(required=False)

    def save(self):
        project = None

        if self.cleaned_data.get('id'):
            project = Project.objects.get(id=self.cleaned_data['id'])
        else:
            project = Project()

        if project:
            project.name = self.cleaned_data['name']
            project.type = self.cleaned_data['type']

            if self.cleaned_data['client'] != None:
                project.client = self.cleaned_data['client']

            if self.cleaned_data['estimated_hours'] != None:
                project.estimated_hours = self.cleaned_data['estimated_hours']

            project.save()
            return project

        return None


#------------------------------------------------------------------------------------------------------------#
class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('description', 'duration', 'type')

    id = forms.IntegerField(required=False)
    projectId = forms.IntegerField(required=True)
    date = forms.DateField(required=True,input_formats=['%Y-%m-%d','%Y/%m/%d'])
    user = User()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TaskForm, self).__init__(*args, **kwargs)

    def clean_projectId(self):
        projectId = self.cleaned_data['projectId']
        if projectId is None:
            raise validators.ValidationError('Error')

        project = Project.objects.get(id=self.cleaned_data['projectId'])

        if project is None:
            raise validators.ValidationError('Error')

        return project

    def save(self):

        if self.cleaned_data.get('id'):
            task = Task.objects.get(id=self.cleaned_data['id'])
        else:
            task = Task()

        project = self.cleaned_data['projectId']
        task.project = project
        task.user = self.user
        task.description = self.cleaned_data['description']
        task.duration = self.cleaned_data['duration']
        task.type = self.cleaned_data['type']
        task.date = self.cleaned_data['date']
        task.save()
        return task
