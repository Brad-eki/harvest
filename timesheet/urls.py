from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'timesheet.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # Todo lo que empiese con uploads se redirecciona a MEDIA_ROOT
    url(r'^$','harvest.views.home'),
    url(r'^home/$','harvest.views.home'),
    url(r'^reports/$','harvest.views.reports'),
    url(r'^timesheet/$','harvest.views.timesheet'),
    url(r'^manage/$','harvest.views.manage'),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^uploads/(?P<path>.*)$','django.views.static.serve',
		{'document_root':settings.MEDIA_ROOT,}
	),
)
