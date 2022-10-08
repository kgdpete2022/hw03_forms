from django.shortcuts import render, get_object_or_404, redirect

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required

from .models import Post, Group, User

from .forms import PostForm


POSTS_PER_PAGE = 10


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
    context = {
        'post': post,
        'author_name': author_name,
        'username': username,
        'posts_count': posts_count,
        'user_posts_link': user_posts_link,
    }
    return render(request, template, context)


@login_required
def post_create(request):    
    form = PostForm(request.POST or None)
    template = 'posts/create_post.html'
    context = {
        'form': form
        }
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', request.user)
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)
    template = 'posts/create_post.html'
    context = {
        'form': form,
        'is_edit': is_edit,
        'post_id': post_id,
        }
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    return render(request, template, context)
