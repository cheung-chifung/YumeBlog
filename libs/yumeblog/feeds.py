from django.contrib.syndication.feeds import Feed,FeedDoesNotExist
from django.core.urlresolvers import reverse
from django.conf import settings

from yumeblog.models import Post,SiteInfo


class LatestPosts(Feed):
    title = lambda s : SiteInfo.objects.get_current().title
    link = lambda s : reverse('blog_index')
    description = lambda s : SiteInfo.objects.get_current().description
    
    def item_link(self,obj):
        return reverse('get_post_by_slug',args=[obj.slug,])
    
    def description(self,obj):
        return obj
        
    def items(self):
        return Post.public_objects.all()[:getattr(settings,'FEED_ITEM_COUNT',10)]
