from django.shortcuts import render, get_object_or_404

from .models import Post, Group, User

from django.core.paginator import Paginator




POSTS_PER_PAGE = 10


# Create your views here.

def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.all()
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)

def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group)
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)

def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts_list = Post.objects.filter(author=author)    
    paginator = Paginator(posts_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts_count = posts_list.count()
    

    context = {
        'username': username,
        'posts_list': posts_list,
        'page_obj': page_obj,
        'posts_count': posts_count,
        'author': author,
        
    }
    return render(request, template, context)

def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = Post.objects.get(pk=post_id)
    author_name = post.author.get_full_name
    username = post.author.username
    posts_count = Post.objects.filter(author=post.author).count()
    user_posts_link = 'profile/' + username   
    context  = {
        'post': post,
        'author_name': author_name,
        'username': username,
        'posts_count': posts_count,
        'user_posts_link': user_posts_link,
    }
    return render(request, template, context)