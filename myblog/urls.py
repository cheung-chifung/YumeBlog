from django.conf.urls.defaults import *

from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    #blog urls
    #(r'^YOUR_INSTANCE_NAME/',include('yumeblog.urls')),
    (r'^myblog/',include('yumeblog.urls')),
)

handler404 = 'yumeblog.views.handler404'
handler500 = 'yumeblog.views.handler500'
