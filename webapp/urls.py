from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    'webapp.views',
    (r'^$', 'viewHome'),
    (r'^participation-form$', 'viewParticipationForm'),
    (r'^home_api/select_section', 'selectHomePageSect')
)

urlpatterns += patterns(
    '',
    (r'^chart_api/', include('city_metrics.ajax_urls')),
)

urlpatterns += patterns(
    '',
    (r'^admin/imports/', include('admin_imports.urls')),
)

urlpatterns += patterns(
    '',
    url(r'^admin/filebrowser/', include('filebrowser.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEVELOPMENT:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^customer_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PROJECT_ROOT + '/customer_media'}),
    )

urlpatterns += patterns(
    'site_content.views',
    url(r'^(?P<aSlug>.*)$', 'viewDetail'),
)