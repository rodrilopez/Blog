from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
import time
from calendar import month_name

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.template import RequestContext

from blog.models import *
from django.forms import ModelForm
from django.template import loader

# Create your views here.



def index(request):
    """Main listing."""
    context = RequestContext(request)
    posts = Post.objects.all().order_by("-created")
    paginator = Paginator(posts, 5)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    context.update(dict(posts=posts, user=request.user,
                        post_list=posts.object_list, months=mkmonth_lst()))
    return render_to_response("list.html", context)





def post(request, id_post):
    """Single post with comments and a comment form."""
    context = RequestContext(request)
    post = Post.objects.get(pk=id_post)
    print request.method
    if 'POST' in request.method:
        author = request.POST['author']
        content = request.POST['content']
    context.update(dict(post=post, user=request.user))
    context.update(csrf(request))
    return render_to_response("post.html", context)

def commentarios(request):
    context = RequestContext(request)
    context['comments'] = Comment.objects.all()
    return render_to_response("_comments.html", context)


def comment(request):
    context = RequestContext(request)
    print "coment"
    if 'POST' in request.method:
        print "if"
        author = request.user
        content = request.POST['comentario']
        comentario = Comment(author=author, 
                             body=content)
        print "entra aca"
        comentario.save()
    #comments = Comment.objects.filter(post=post)
    #context.update(dict(user=request.user, comments=comments))
    #context.update(csrf(request))
    return redirect ('/')
    return render_to_response('coments.html',context)




def mkmonth_lst():
    """Make a list of months to show archive links."""
    if not Post.objects.count(): return []

    # set up vars
    year, month = time.localtime()[:2]
    first = Post.objects.order_by("created")[0]
    fyear = first.created.year
    fmonth = first.created.month
    months = []

    # loop over years and months
    for y in range(year, fyear-1, -1):
        start, end = 12, 0
        if y == year: start = month
        if y == fyear: end = fmonth-1

        for m in range(start, end, -1):
            months.append((y, m, month_name[m]))
    return months







def month(request, year, month):
    """Monthly archive."""
    posts = Post.objects.filter(created__year=year, created__month=month)
    return render_to_response("list.html", dict(post_list=posts, user=request.user,
                                                months=mkmonth_lst(), archive=True))
