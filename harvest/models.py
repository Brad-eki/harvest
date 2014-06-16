from django.db import models
from django.contrib.auth.models import User
from timesheet import settings
from django.core.files import File
from PIL import Image
from harvest.general.storage import OverwriteStorage

# Create your models here. settings.MEDIA_ROOT

def only_filename(instance, filename):
    return filename

class ManyToManyField_NoSyncdb(models.ManyToManyField):
    def __init__(self, *args, **kwargs):
        super(ManyToManyField_NoSyncdb, self).__init__(*args, **kwargs)
        self.creates_table = False

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

    id = models.AutoField(primary_key=True)
    users = models.ManyToManyField(User, related_name='users',db_table='harvest_projects_users')
    name = models.CharField(max_length=50)
    client = models.CharField(max_length=50,blank=True)
    type = models.CharField(max_length=20,choices=PROJECT_TYPE)
    estimated_hours = models.PositiveIntegerField(default=0,blank=True)
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
        ('Bug Fix','Bug Fix'),
        ('Client Support','Client Support'),
        ('Development','Development'),
        ('Design','Design'),
        ('Management','Management'),
        ('Other','Other'),
        ('Research','Research'),
        ('Rework','Rework'),
        ('Testing','Testing'),
    )

    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=30,choices=TASK_TYPE,blank=False)
    duration = models.DecimalField(max_digits=5,decimal_places=2,blank=False)
    date = models.DateField()
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'tasks'
        ordering = ['-modified']


User.add_to_class('thumbnail', models.ImageField(storage=OverwriteStorage(),upload_to = only_filename ))
User.add_to_class('projects', ManyToManyField_NoSyncdb(Project, related_name='projects',db_table='harvest_projects_users'))
