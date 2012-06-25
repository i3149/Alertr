from django.conf.urls import patterns, include, url

from fs.views.time import current_datetime
from fs.views.data import init_user
from fs.views.data import handle_alert

# Admin code
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   (r'^time/$', current_datetime),
   (r'^data/$', init_user),
   (r'^data/(.+)/$', handle_alert), 

    # Examples:
    # url(r'^$', 'fs.views.home', name='home'),
    # url(r'^fs/', include('fs.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
