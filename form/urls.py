from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'questionnaire.views.home', name='home'),
    url(r'^form/([0-9]*)/$','questionnaire.views.form', name='form'),
    url(r'^form_submit/([0-9]*)/$','questionnaire.views.form_submit', name='form_submit'),
    url(r'^statistic/([0-9]*)/$','questionnaire.views.statistic', name='statistic'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/admin-move/(?P<direction>\w+)/(?P<model_type_id>\w+)/(?P<model_id>\w+)/$',name='admin-move'),
    url(r'^admin/', include(admin.site.urls)),
)
