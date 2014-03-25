from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Project(models.Model):

    PROJECT_TYPE=(
        ('Android','Android'),
        ('Blackberry','Blackberry'),
        ('iPad','iPad'),
        ('iPhone','iPhone'),
        ('iPhone/iPad','iPhone/iPad'),
        ('Windows Phone','Windows Phone'),
        ('Flash','Flash'),
        ('Backend/WS','Backend/WS'),
        ('Web','Web'),
        ('.Net','.Net'),
        ('Other','Other'),
    )

    user = models.ManyToManyField(User)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20,choices=PROJECT_TYPE)
    estimated_hours = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'project'
        verbose_name_plural = 'projects'
        ordering = ['name']


class Task(models.Model):

    TASK_TYPE=(
        ('Admin','Admin'),
        ('Bug Fix','Bug Fix'),
        ('Client Support','Client Support'),
        ('Development','Development'),
        ('Graphic Design','Graphic Design'),
        ('Other','Other'),
        ('Project Managment','Project Managment'),
        ('Research','Research'),
        ('Rework','Rework'),
        ('Testing','Testing'),
    )

    user = models.OneToOneField(User)
    project = models.OneToOneField(Project)
    description = models.TextField()
    type = models.CharField(max_length=30,choices=TASK_TYPE)
    duration = models.TimeField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'tasks'
        ordering = ['-created']