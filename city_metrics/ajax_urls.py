from django.conf.urls import *

urlpatterns = patterns('city_metrics.ajax_views',
                       (r'^update-chart', 'update_chart'),
)