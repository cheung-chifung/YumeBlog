from django.contrib import admin
from yumeblog.models import Post,Page,Link,Menu,SiteInfo,Comment
from django.conf import settings

from django.utils.translation import ugettext as _

class PostAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','slug','tags','is_public','created')
    fieldsets = (
        (None, {'fields': ('title', 'slug','tags',)}),
        (_('Content'), {'fields': ('content', 'intro',)}),
        (_('Meta'), {'fields': ('is_public', 'created','site',)}),
    )
    search_fields = ['title','intro',]
    list_filter = ['is_public','created',]
    date_hierarchy = 'created'
    prepopulated_fields = {"slug": ("title",)}
    
class PageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','slug','created')
    fieldsets = (
        (None, {'fields': ('title', 'slug',)}),
        (_('Content'), {'fields': ('content',)}),
        (_('Meta'), {'fields': ('created','site')}),
    )
    search_fields = ['title',]
    list_filter = ['created',]
    date_hierarchy = 'created'
    prepopulated_fields = {"slug": ("title",)}
    
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title','url','relation')
    fieldsets = (
        (None, {'fields': ('title', 'url',)}),
        (_('Meta'), {'fields': ('relation','site',)}),
    )
    search_fields = ['title','url']
    
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title','url')
    fieldsets = (
        (None, {'fields': ('title', 'url',)}),
        (_('Meta'), {'fields': ('site',)}),
    )
    search_fields = ['title','url',]

class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ('title','subtitle','description')
    fieldsets = (
        (None, {'fields': ('title', 'subtitle',)}),
        (_("Detail"), {'fields': ('description', 'copyright','copyright_plain_text','keywords',)}),
        (_('Meta'), {'fields': ('site',)}),
    )
    search_fields = ['title','subtitle',]
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name','user_url','comment')
    fieldsets = (
        (None, {'fields': ('user_name', 'user_email', 'user_url',)}),
        (_('Meta'), {'fields': ('is_public','site',)}),
    )
    search_fields = ['user_name','comment']
    
admin.site.register(SiteInfo,SiteInfoAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(Link,LinkAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Menu,MenuAdmin)
