from django.db import models

from fckeditor.fields import RichTextField
from tagging.fields import TagField
from django.contrib.sites.models import Site

from datetime import datetime

from django.utils.translation import ugettext as _
from django.contrib.sites.managers import CurrentSiteManager
from django.conf import settings

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH',3000)

class SiteInfoManager(models.Manager):
    def get_current(self):
        return SiteInfo.objects.filter(site = Site.objects.get_current())[0]

class SiteInfo(models.Model):
    title = models.CharField(_('Title'),max_length=100)
    subtitle = models.CharField(_('Subtitle'),max_length=255)
    description = models.TextField(_('description'))
    copyright = models.TextField(_('Copyright in HTML'))
    copyright_plain_text = models.CharField(_('Copyright in Plain Text'),max_length=250,null=True,blank=True)
    keywords = models.CharField(_('Keyword'),max_length=100)
    site = models.OneToOneField(Site,default=settings.SITE_ID)
    feed = models.URLField(_('Custom Feed URL'), blank=True)
    
    objects = SiteInfoManager()
    
    def __unicode__(self):
        return self.title

class Menu(models.Model):
    "Navi-bar"
    title = models.CharField(_("Title"),max_length=255)
    url = models.CharField(_('URL'),max_length=255)
    site = models.ForeignKey(Site,default=settings.SITE_ID)
    objects = CurrentSiteManager()
    
    def __unicode__(self):
        return self.title

class Link(models.Model):
    "Links"
    title = models.CharField(_("Title"),max_length=255)
    url = models.URLField(_("URL"),max_length=255)
    relation = models.CharField(_("Type"),default='friend',max_length=20)
    site = models.ForeignKey(Site,default=settings.SITE_ID)
    description = models.TextField(_('description'))
    objects = CurrentSiteManager()
    
    def __unicode__(self):
        return self.title

class Page(models.Model):
    "Blog's page"
    title = models.CharField(_("Title"),max_length=255)
    slug = models.SlugField(_("Slug"),max_length=255)
    content = RichTextField(_("Content"))
    site = models.ManyToManyField(Site,default=[settings.SITE_ID,])
    objects = CurrentSiteManager()
    updated = models.DateTimeField(_("Modified"),auto_now=True)
    created = models.DateTimeField(_("Created"),default=datetime.now())

    class Meta:
        ordering = ['-created']
        
    def __unicode__(self):
        return self.title

class PublicPostManager(CurrentSiteManager):
    def get_query_set(self):
        return super(PublicPostManager,self).get_query_set().filter(is_public=True)

class Post(models.Model):
    "Blog's posts"
    title = models.CharField(_("Title"),max_length=255)
    slug = models.SlugField(_("Slug"),max_length=255)
    content = RichTextField(_("Content"))
    intro = RichTextField(_("Brief introduction"),null=True,blank=True)
    tags = TagField(_("Tags"))
    
    site = models.ForeignKey(Site,default=settings.SITE_ID)
    objects = CurrentSiteManager()
    public_objects = PublicPostManager()

    is_public = models.BooleanField(_('is public'), default = True)
    
    updated = models.DateTimeField(_("Modified"),auto_now=True)
    created = models.DateTimeField(_("Created"),default=datetime.now())

    class Meta:
        ordering = ['-created','-id',]
        
    def __unicode__(self):
        return self.title

#TODO
#class CommentManager(CurrentSiteManager):
#    pass

class Comment(models.Model):
    "Post's Comment"
    user_name   = models.CharField(_("name"), max_length=50)
    user_email  = models.EmailField(_("email address"))
    user_url    = models.URLField(_("homepage"), blank=True)
    
    comment = models.TextField(_('comment'), max_length=COMMENT_MAX_LENGTH)
    
    ip_address  = models.IPAddressField(_('ip address'), blank=True, null=True)
    #user_agent   = models.CharField(_("user's name"), max_length=100)
    
    post = models.ForeignKey(_('post'))
    parent = models.ForeignKey('self',related_name='children',default=None,null=True,blank=True)
    
    site = models.ForeignKey(Site,default=settings.SITE_ID)
    objects = CurrentSiteManager()
    
    is_public = models.BooleanField(_('is public'), default = True)
    is_notice = models.BooleanField(_('receive email notify'), default = True)
    
    updated = models.DateTimeField(_("Modified"),auto_now=True)
    created = models.DateTimeField(_("Created"),default=datetime.now())
    
    #Inspired by http://www.djangosnippets.org/snippets/112/
    # &http://www.voidspace.org.uk/python/modules.shtml#akismet
    def comment_check(self):
        '''
        Check a comment.
        Return True for ham, False for spam.
        Use this function before save a comment.
        '''
        try:
            if hasattr(settings, 'BAN_NON_CJK') and settings.BAN_NON_CJK:
                import re
                if not re.search(ur"[\u4E00-\u9FC3\u3041-\u30FF]",self.comment):
                    raise Exception()
                
            if hasattr(settings, 'AKISMET_API_KEY') and settings.AKISMET_API_KEY:
                from akismet import Akismet
                akismet_api = Akismet(key=settings.AKISMET_API_KEY, blog_url='http://%s/' % Site.objects.get_current().domain)
                if akismet_api.verify_key():
                    akismet_data = { 'comment_type': 'comment',
                                    'user_ip':self.ip_address,
                                    'user_agent':self.user_agent,
                                    'referrer':'',
                                    }
                    return not akismet_api.comment_check(self.comment.encode("utf8"), data=akismet_data, build_data=True)
            else:
                return True
        except:
            return False

    class Meta:
        ordering = ['-created']
        
    def __unicode__(self):
        return self.comment
    
from django.db.models import signals
from django.dispatch import dispatcher

from models import Comment
