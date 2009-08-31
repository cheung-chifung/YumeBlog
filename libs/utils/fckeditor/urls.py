from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^fckeditor/editor/fckeditor_connector/browser/$', 'fckeditor.connector.views.browser'),
    (r'^fckeditor/editor/fckeditor_connector/uploader/$', 'fckeditor.connector.views.uploader'),
    url(r'^fckeditor/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.FCKEDITOR_MEDIA_ROOT},name='get_fckeditor_media_files'),
)
