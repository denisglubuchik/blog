from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm

# Create your views here.
def index(request):
    return render(request, 'blogs/index.html')

def posts(request):
    posts = BlogPost.objects.order_by('-date_added')
    context = {'posts': posts}
    return render(request, 'blogs/posts.html', context)

@login_required
def post(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    comments = post.comment_set.order_by('-date_added')
    context = {'post': post, 'comments': comments}
    return render(request, 'blogs/post.html', context)

@login_required
def new_post(request):
    if request.method != 'POST':
        form = BlogPostForm()
    else:
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return redirect('blogs:posts')
    
    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)

@login_required
def edit_post(request, post_id):
    post = BlogPost.objects.get(id=post_id)

    if post.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = BlogPostForm(instance=post)
    else:
        form = BlogPostForm(instance=post, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('blogs:posts')
    
    context = {'post': post,'form': form}
    return render(request, 'blogs/edit_post.html', context)

@login_required
def new_comment(request, post_id):
    post = BlogPost.objects.get(id=post_id)

    if request.method != 'POST':
        form = CommentForm()
    else:
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.owner = request.user
            new_comment.post = post
            form.save()
            return redirect('blogs:post', post_id=post.id)
        
    context = {'post': post, 'form': form}
    return render(request, 'blogs/new_comment.html', context)

@login_required
def edit_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    post = comment.post

    if comment.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        form = CommentForm(instance=comment)
    else:
        form = CommentForm(instance=comment, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('blogs:post', post_id=post.id)
        
    context = {'post': post, 'comment': comment, 'form': form}
    return render(request, 'blogs/edit_comment.html', context)