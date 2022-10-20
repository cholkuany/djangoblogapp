from django.shortcuts import render
from app.forms import CommentForm, SubscribeForm, CreateUser
from django.http import HttpResponseRedirect
from app.models import BlogMeta, Comment, Post, Profile, Tag
from django.urls import reverse
from django.db.models import Count
from django.contrib.auth.models import User



from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
# @login_required(login_url='login_page')
def index(request):
    posts = Post.objects.all()
    top_posts = Post.objects.all().order_by('-view_count')[0:3]
    recent_posts = Post.objects.all().order_by('-last_updated')[0:3]
    featured_blog = Post.objects.filter(is_featured = True)
    subscribe_form = SubscribeForm()
    subscribe_successful = None
    blogMeta = None

    if featured_blog:
        featured_blog = featured_blog[0]

    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            subscribe_successful = "Subscribe successful"
            subscribe_form = SubscribeForm()
    if BlogMeta.objects.all().exists():
        blogMeta = BlogMeta.objects.all()[0]

    context = {
        'posts': posts, 
        'top_posts': top_posts, 
        'recent_posts': recent_posts,
        'subscribe_form': subscribe_form,
        'subscribe_successful': subscribe_successful,
        'featured_blog': featured_blog,
        'blogMeta': blogMeta,
        }
    return render(request, 'app/index.html', context)

# @login_required(login_url='login_page')
def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comment.objects.filter(post=post, parent=None)
    form = CommentForm()

    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_obj = None
            if request.POST.get('parent'):
                #save reply
                parent = request.POST.get('parent')
                parent_obj = Comment.objects.get(id=parent)
                if parent_obj:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent_obj
                    comment_reply.post = post
                    comment_reply.save()
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))
            else:
                comment = comment_form.save(commit=False)
                postid = request.POST.get("post_id")
                post = Post.objects.get(id=postid)
                comment.post = post
                comment.save()

                return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))

        

    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count = post.view_count + 1
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, 'app/post.html', context)

# @login_required(login_url='login_page')
def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    top_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-view_count')[0:3]
    recent_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-last_updated')[0:3]
    
    tags = Tag.objects.all()
    context = {'tag': tag, 'top_posts': top_posts, 'recent_posts': recent_posts, 'tags': tags}
    return render(request, 'app/tag.html', context)

def author_page(request, slug):
    author = Profile.objects.get(slug=slug)
    top_posts = Post.objects.filter(author__in=[author.id]).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(author__in=[author.id]).order_by('-last_updated')[0:3]

    top_authors = User.objects.annotate(number=Count('post')).order_by('-number')

    context = {
        'author': author, 
        'top_posts': top_posts, 
        'recent_posts': recent_posts,
        'top_authors': top_authors
        }
    return render(request, 'app/author.html', context)

# @login_required(login_url='login_page')
def login_page(request):
    if request.user.is_authenticated:
        return reverse('index')
        
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return reverse('index')
        else:
            messages.info(request, 'Username OR passwrod is incorrect')
    context = {}
    return render(request, 'app/login.html', context)

def logout_page(request):
    logout(request)
    return reverse('login_page')

def register_page(request):
    if request.user.is_authenticated:
        return reverse('index')

    form = CreateUser()
    if request.POST:
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {user}')
            
    context = {'form': form}
    return render(request, 'app/register.html', context)

def search_page(request):
    search_query = ''
    if request.GET.get('q'):
        search_query = request.GET.get('q')
    filtered_posts = Post.objects.filter(title__icontains=search_query)
    context = {
        'search_query': search_query,
        'filtered_posts': filtered_posts,
        }

    return render(request, 'app/search.html', context)