from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'timesheet.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # Todo lo que empiese con uploads se redirecciona a MEDIA_ROOT
    url(r'^$','harvest.views.home'),
    url(r'^welcome/$','harvest.views.home'),

    url(r'^reports/$', RedirectView.as_view(url='/reports/users/'), name='reports_user_redirect'),
    url(r'^reports/users/$','harvest.views.reports_user_list'),
    url(r'^reports/projects/$','harvest.views.reports_project_list'),
    url(r'^reports/users/[0-9]*$','harvest.views.user_report'),
    url(r'^reports/projects/[0-9]*$','harvest.views.project_report'),

    url(r'^timesheet/$','harvest.views.timesheet'),

    url(r'^manage/$', RedirectView.as_view(url='/manage/users/'), name='manage_user_redirect'),
    url(r'^manage/users/$','harvest.views.admin_user_list'),
    url(r'^manage/projects/$','harvest.views.admin_project_list'),
    url(r'^manage/users/[0-9]*$','harvest.views.admin_user'),
    url(r'^manage/projects/edit/[0-9]*$','harvest.views.edit_project'),
    url(r'^manage/users/new$','harvest.views.admin_create_user'),
    url(r'^manage/users/archived/','harvest.views.admin_archived_users'),
    url(r'^manage/projects/new$','harvest.views.admin_create_project'),
    url(r'^manage/projects/archived/','harvest.views.admin_archived_projects'),

    url(r'^login/$','harvest.views.login'),
    url(r'^manage/user/edit/[0-9]*$','harvest.views.edit_user_profile'),

	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^uploads/(?P<path>.*)$','django.views.static.serve',
		{'document_root':settings.MEDIA_ROOT,}
	),
)
