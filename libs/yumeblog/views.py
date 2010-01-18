from models import Post,Page,Comment,SiteInfo
from forms import CommentForm
from tagging.models import Tag,TaggedItem

from django.conf import settings

from django.utils.translation import ugettext as _

from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.http import Http404,HttpResponse,HttpResponseRedirect

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.core.mail import EmailMessage

from django.db.models import Q
from hashlib import md5

from useragent.uasparser import UASparser

def show_post(request,template_name='post.htm',pk=None,slug=None):
    '''
    Show a single post by post's slug or primarykey
    '''
    msg = {'message':'',
           'type_str':'',
           'type_code':'',
           }

    try:
        if slug is not None:
            post = Post.public_objects.get(slug=slug)
        else:
            post = Post.public_objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        lastest_comment = md5(request.POST['comment'].encode('utf-8')).hexdigest()
        if request.session.get('LASTEST_COMMENT','') == lastest_comment :
            msg['message'] = _('You\'ve already commented.')
            msg['type_str'] = _('Alert')
            msg['type_code'] = 'ALERT'
        elif form.is_valid():
            #before save
            comment = form.save(commit=False)
            comment.post = post
            comment.ip_address = request.META['REMOTE_ADDR']
            
            if comment.comment_check(): #Start Moderation
                #fetch user agent string
                uas_parser = UASparser()
                uas_data = uas_parser.parse(request.META['HTTP_USER_AGENT'])
                comment.useragent = "%s||%s" % ( uas_data['ua_name'], uas_data['os_name'] )
                
                #save
                comment.save()

                #send notify
                msg['message'] = _('Your comment has submited successfully.')
                msg['type_code'] = 'SUCCESS'
                request.session['LASTEST_COMMENT'] = md5(comment.comment.encode('utf8')).hexdigest()
                if comment.parent and comment.parent.is_notice: #Send mail
                    from settings import EMAIL_HOST_USER
                    site = SiteInfo.objects.get_current()
                    subject = _("Your comment over at %s now have new reply" % site.title)
                    html_content = loader.render_to_string("email-notify.htm",{
                                                                'site':site,
                                                                'post':post,
                                                                'original':comment.parent,
                                                                'reply':comment,
                                                                               })
                    recipient_list = [comment.parent.user_email,]
                    mail = EmailMessage(subject, html_content, EMAIL_HOST_USER, recipient_list)
                    mail.content_subtype = "html"
                    mail.send()
            else:
                comment.is_public = False
                if hasattr(settings, 'DELETE_SPAM_COMMENT') and not settings.DELETE_SPAM_COMMENT:
                    comment.save()
                msg['message'] = _('Your comment is under medoration.')
                msg['type_str'] = _('Submitd')
                msg['type_code'] = 'ALERT'
            
            form = CommentForm()
                
        else:
            print form
            msg['message'] = _('Please check the form and try again.')
            msg['type_str'] = _('Submit failed')
            msg['type_code'] = 'ERROR'
        
    else:
        form = CommentForm()
        
    try:    #Try to initial user info to form
        if ( request.COOKIES.has_key('BLOG_USERNAME') and 
             request.COOKIES.has_key('BLOG_USEREMAIL') and 
             request.COOKIES.has_key('BLOG_USERURL') and
            request.COOKIES.has_key('IS_NOTICE') ):
            form = CommentForm(initial={
                            'user_name':request.COOKIES['BLOG_USERNAME'],
                            'user_email':request.COOKIES['BLOG_USEREMAIL'],
                            'user_url':request.COOKIES['BLOG_USERURL'],
                            'is_notice':request.COOKIES['IS_NOTICE'],
                            })
    except:
        pass
    
    response = render_to_response(template_name,
                              {'post':post,
                               'form':form,
                               'msg':msg,
                               },
                              context_instance=RequestContext(request))
    try:
        max_age = 3600*24*365
        response.set_cookie('BLOG_USERNAME', comment.user_name, max_age)
        response.set_cookie('BLOG_USEREMAIL', comment.user_email, max_age)
        response.set_cookie('BLOG_USERURL', comment.user_url, max_age)
        response.set_cookie('IS_NOTICE', comment.is_notice, max_age)
    except:
        pass
        
    return response
        

def show_page(request,template_name='page.htm',slug=None):
    '''
    Show a single page by post's slug or primarykey
    '''
    try:
        if slug is not None:
            page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        raise Http404
    return render_to_response(template_name,
                              {'page':page},
                              context_instance=RequestContext(request))

def list_post(request,template_name='list.htm',tag=None,keyword=None):
    '''
    List post by tag or keyword
    '''

    # check if tag available
    if tag is None:
        post_list = Post.public_objects.all()
        if keyword is not None:
            post_list = post_list.filter(
                            Q(title__contains=keyword)|
                            Q(content__contains=keyword)
                        )
    else:
        tag = Tag.objects.get(name=tag)
        post_list = TaggedItem.objects.get_by_model(Post,tag).filter(is_public=True)
    paginator = Paginator( post_list, getattr(settings, 'ITEM_COUNT_PER_PAGE', 8))
    
    # setup the pagination
    try:
        page = int(request.GET.get('page',1))
    except ValueError:
        page = 1
    
    try:
        posts = paginator.page(page)
    except ( EmptyPage, InvalidPage ):
        posts = paginator.page(paginator._num_pages)
      
    if tag is not None:
        posts.list_by = tag
        posts.list_type = 'TAG'
    elif keyword is not None:
        posts.list_by = keyword
        posts.list_type = 'SEARCH'
    # render the template
    return render_to_response(template_name,
                              {'posts':posts},
                              context_instance=RequestContext(request))
                              
def handler404(request):
    return show_page(request,slug='404')
    
def handler500(request):
    return show_page(request,slug='500')
