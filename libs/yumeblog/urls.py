from django.conf.urls.defaults import *
from django.conf import settings

from yumeblog.feeds import LatestPosts

from django.contrib import admin
admin.autodiscover()
import os

feeds = { 'latest': LatestPosts, }

urlpatterns = patterns('',   
   (r'^fckeditor/',include('fckeditor.urls')),
   
   #index
   url(r'^index$','yumeblog.views.list_post',{'template_name':'list.htm'},name='blog_index'),
   
   #static files
   (r'^admin/(.*)', admin.site.root),
   (r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
   (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
   url(r'^style/(?P<path>.*)$','django.views.static.serve',{'document_root':os.path.join(settings.TEMPLATE_BLOG_ROOT,'style')},name='get_blog_media_file'),

   #post list
   url(r'^tag/(?P<tag>[^/]+)/$','yumeblog.views.list_post',{'template_name':'list.htm'},name='list_post_by_tag'),
   url(r'^search/(?P<keyword>[^/]+)/$','yumeblog.views.list_post',{'template_name':'list.htm'},name='list_post_by_keyword'),
   url(r'^$','yumeblog.views.list_post',{'template_name':'list.htm'},name="list_post"),
   
   #comments
   
   #feeds
   url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',{'feed_dict': feeds},name="get_feed"),
   
   #page
   url(r'^page/(?P<slug>\S+)/$', 'yumeblog.views.show_page',{'template_name':'page.htm'},name="get_page_by_slug"),
   
   #single post
   url(r'^(?P<pk>\d+)/$', 'yumeblog.views.show_post',{'template_name':'post.htm'},name="get_post_by_id"),
   url(r'^(?P<slug>\S+)/$', 'yumeblog.views.show_post',{'template_name':'post.htm'},name="get_post_by_slug"),
   
)

handler404 = 'yumeblog.views.handler404'
handler500 = 'yumeblog.views.handler500'

