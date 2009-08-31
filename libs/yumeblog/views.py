from models import Post,Page,Comment
from forms import CommentForm
from tagging.models import Tag,TaggedItem

from django.conf import settings

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404,HttpResponse,HttpResponseRedirect

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.db.models import Q
from hashlib import md5

def show_post(request,template_name='post.htm',pk=None,slug=None):
    '''
    Show a single post by post's slug or primarykey
    '''
    msg = {'message':'',
           'type_str':'',
           'type_code':0,     # 0 for None; 1 for normal message; 2 for alert; 3 for Error
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
            msg['message'] = 'You\'ve already commented.'
            msg['type_str'] = 'Alert'
            msg['type_code'] = 3
        elif form.is_valid():
            #before save
            comment = form.save(commit=False)
            comment.post = post
            comment.ip_address = request.META['REMOTE_ADDR']
            comment.user_agent = request.META['HTTP_USER_AGENT']
            if comment.comment_check(): #Start Moderation
                comment.save()
                msg['message'] = 'Your comment has submited successfully.'
                msg['type_code'] = 1
                request.session['LASTEST_COMMENT'] = md5(comment.comment.encode('utf8')).hexdigest()
                
            else:
                comment.is_public = False
                if hasattr(settings, 'DELETE_SPAM_COMMENT') and not settings.DELETE_SPAM_COMMENT:
                    comment.save()
                msg['message'] = 'Your comment is under medoration.'
                msg['type_str'] = 'Submitd'
                msg['type_code'] = 2
            
            form = CommentForm()
                
        else:
            msg['message'] = 'Please check the form and try again.'
            msg['type_str'] = 'Submit failed'
            msg['type_code'] = 3
        
    else:
        form = CommentForm()
        
    try:    #Try to initial user info to form
        if request.COOKIES.has_key('BLOG_USERNAME') and request.COOKIES.has_key('BLOG_USEREMAIL') and request.COOKIES.has_key('BLOG_USERURL'):
            form = CommentForm(initial={
                            'user_name':request.COOKIES['BLOG_USERNAME'],
                            'user_email':request.COOKIES['BLOG_USEREMAIL'],
                            'user_url':request.COOKIES['BLOG_USERURL'],
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
        response.set_cookie('BLOG_USERNAME',comment.user_name,max_age)
        response.set_cookie('BLOG_USEREMAIL',comment.user_email,max_age)
        response.set_cookie('BLOG_USERURL',comment.user_url,max_age)
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
    except ( EmptyPage, InvalidPage):
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
