from django.template import Library, Node, TemplateSyntaxError
from django.db.models import get_model
from django.utils.translation import ugettext as _
from yumeblog.models import Post,SiteInfo,Comment
from yumeblog.forms import CommentForm

from tagging.models import TaggedItem

from hashlib import md5
from django.utils.safestring import mark_safe
import urllib

register = Library()
     
class LatestContentNode(Node):
    def __init__(self, model, varname, num=0):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        context[self.varname] = self.model.objects.all()
        if(self.num!=0):
            context[self.varname] = context[self.varname][:self.num]
        return ''

class RelatedPostNode(Node):
    def __init__(self, instance, varname, num=0):
        self.num, self.varname, self.instance = num, varname, instance
        
    def render(self, context):
        context[self.varname] = TaggedItem.objects.get_related(self.instance.resolve(context),Post)

        return ''
    
@register.tag
def get_related_posts(parser, token):
    bits = token.contents.split()
    if len(bits) < 5 or bits[3] != 'as':
        raise TemplateSyntaxError, _("Invaild tag syntax excepted {% get_related_posts POST NUM as VARNAME%} or {% get_related_posts POST ALL as VARNAME %}")
    num = bits[2].upper() == 'ALL' and None or bits[2]
    return RelatedPostNode(parser.compile_filter(bits[1]), bits[4], num)

@register.tag
def get_latest(parser, token):
    bits = token.contents.split()
    if len(bits) < 5 or bits[3] != 'as':
        raise TemplateSyntaxError, _("Invaild tag syntax excepted {% get_latest APP.MODEL NUM as VARNAME%} %}")
    return LatestContentNode(bits[1], bits[4], bits[2])

class LatestCommentNode(Node):
    def __init__(self, varname, num=0):
        self.num, self.varname = num, varname
    
    def render(self, context):
        context[self.varname] = Comment.objects.filter(is_public=True).order_by('-updated')

        if(self.num!=0):
            context[self.varname] = context[self.varname][:self.num]
        return ''

@register.tag
def get_latest_comments(parser, token):
    bits = token.contents.split()
    if len(bits) < 4 or bits[2] != 'as':
        raise TemplateSyntaxError, _("Invaild tag syntax excepted {% get_latest_comments NUM as VARNAME%} %}")
    return LatestCommentNode(bits[3], bits[1])

@register.tag
def get_menuitems(parser,token):
    bits = token.contents.split()
    if len(bits) < 3 or bits[1] != 'as':
        raise TemplateSyntaxError, _("Invaild tag syntax excepted {% get_menuitems as VARNAME%}")
    return LatestContentNode('yumeblog.menu',bits[2])

class GetCommentCountNode(Node):
    def __init__(self, post, varname):
        self.varname = varname
        self.post = post
        
    def render(self, context):
        context[self.varname] = Comment.objects.filter(post=context[self.post],is_public=True).count()
        return ''
    
@register.tag
def get_comments_count(parser,token):
    bits = token.contents.split()
    if len(bits) < 5 or bits[3] != 'as' or bits[1] != 'for':
        raise TemplateSyntaxError, _("Invaild tag syntax excepted {% get_comments_count for POST as VARNAME%}")
    return GetCommentCountNode(bits[2],bits[4])

class GetCommentNode(Node):
    def __init__(self, post, varname):
        self.varname = varname
        self.post = post
        
    def render(self, context):
        context[self.varname] = Comment.objects.filter(post=context[self.post],is_public=True).order_by('created')
        return ''

@register.tag
def get_comments(parser,token):
    bits = token.contents.split()
    if len(bits) < 5 or bits[3] != 'as' or bits[1] != 'for':
        raise TemplateSyntaxError, _("Invaild tag syntax excepted {% get_comments for POST as VARNAME%}")
    return GetCommentNode(bits[2],bits[4])

class CommentFormNode(Node):
    def __init__(self, varname):
        self.varname = varname
        
    def render(self, context):
        context[self.varname] = CommentForm()
        return ''

@register.tag
def get_comment_form(parser, token):
    bits = token.contents.split()
    if len(bits) < 3 or bits[1] != 'as':
        raise TemplateSyntaxError, _("Invaild tag syntax excepted {% get_comment_form as VARNAME%}")
    return CommentFormNode(bits[2])

class SiteInfoContentNode(Node):
    def __init__(self, varname):
        self.varname = varname
    
    def render(self, context):
        context[self.varname] = SiteInfo.objects.get_current()
        return ''
    
@register.tag
def get_siteinfo(parser, token):
    bits = token.contents.split()
    if len(bits) < 3 or bits[1] != 'as':
        raise TemplateSyntaxError, _("Invaild tag syntax excepted {% get_siteinfo as VARNAME%}")
    return SiteInfoContentNode(bits[2])

from django import template

#Refer to http://en.gravatar.com/site/implement/url
class GravatarURLNode(Node):
    GRAVATAR_URL = u'http://www.gravatar.com/avatar/%(hashed_email)s?r=%(rating)s&s=%(size)s&d=%(default)s'
    
    def __init__(self,email,size,rating,default):
        self.email = email
        self.size = size 
        self.rating = rating
        self.default = default
    
    def render(self, context):
        hashed_email = md5(self.email.resolve(context).lower()).hexdigest()
        self.url = mark_safe(self.GRAVATAR_URL % ({
            'hashed_email':hashed_email,
            'size':self.size.resolve(context),
            'rating':self.rating.resolve(context),
            'default':urllib.quote_plus(self.default)
            }))
        return self.url
    
@register.tag
def gravatar_url(parser, token):
    bits = token.contents.split()
    if len(bits) < 5:
        raise TemplateSyntaxError, _("Invaild tag syntax excepted {% gravatar EMAIL SIZE(1-512) 'RATING'(g/r/pg/x) DEFAULT(identicon/monsterid/wavatar/404/your_default_image_url) %}")

    email,size,rating,default = bits[1:5]
    return GravatarURLNode(
            parser.compile_filter(email),
            parser.compile_filter(size),
            parser.compile_filter(rating),
            default)
 
#Inspired by Lucas Murray's work. http://www.undefinedfire.com/lab/recursion-django-templates/
class NestedCommentNode(Node):
    def __init__(self, rows, root, varname, node_list):
        self.varname = varname
        self.node_list = node_list
        self.rows = rows
        self.root = root
    
    def renderCallBack(self, context, root_id, rows, depth):
        output = []
        children = [row['data'] for row in rows if row['parent_id'] == root_id]
        if len(children):
            if 'loop' in self.node_list:
                output.append(self.node_list['loop'].render(context))
            for child in children:
                context.push()
                context['depth'] = depth
                context[self.varname] = child
                if 'children' in self.node_list:
                    output.append(self.node_list['children'].render(context))
                    output.append(self.renderCallBack(context, child.pk, rows, depth+1))
                if 'endloop' in self.node_list:
                    output.append(self.node_list['endloop'].render(context))
                else:
                    output.append(self.node_list['end_nested_comment'].render(context))
                context.pop()
            if 'endloop' in self.node_list:
                output.append(self.node_list['end_nested_comment'].render(context))
        return ''.join(output)
            
    
    def render(self, context):
        rows = [{'data':row,'id':row.pk,'parent_id':row.parent and row.parent.pk or None} for row in self.rows.resolve(context)]
        root = self.root and self.root.resolve(context) or None
        output = self.renderCallBack(context, root, rows, 1)
        return output

#Inspired by Lucas Murray's work. http://www.undefinedfire.com/lab/recursion-django-templates/
@register.tag
def nested_comment(parser, token):
    bits = list(token.split_contents())
    if (len(bits)==4 and bits[2] != 'as') or (len(bits)==5 and bits[3] != 'as') or len(bits) not in [4,5,]:
        raise template.TemplateSyntaxError, "Invalid tag syxtax expected '{% nested_comment COMMENTS as COMMENT%}' or '{% nested_comment COMMENTS ROOT as COMMENT%}'"
    
    if len(bits)==4:
        varname = bits[3]
        root = None
    else:
        varname = bits[4]
        root = parser.compile_filter(bits[2])
        
    rows = parser.compile_filter(bits[1])

    node_list = {}
    while len(node_list) < 4:
        temp = parser.parse(('end_nested_comment','children','loop','endloop'))
        tag = parser.tokens[0].contents
        node_list[tag] = temp
        parser.delete_first_token()
        if tag == 'end_nested_comment':
            break
    return NestedCommentNode(rows, root, varname, node_list)


