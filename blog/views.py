from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Post, Category, Tag, Comment
from .forms import PostForm, CommentForm, SearchForm

def is_author(user):
    return user.groups.filter(name='Authors').exists() or user.is_staff

def home(request):
    posts_list = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
    
    # Search functionality
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        
        if query:
            posts_list = posts_list.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query)
            )
        
        if category:
            posts_list = posts_list.filter(category=category)
    
    # Pagination
    paginator = Paginator(posts_list, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'blog/home.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(is_approved=True)
    
    # Handle comment submission
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to comment.')
            return redirect('login')
        
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
            return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/post_detail.html', context)

def posts_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts_list = Post.objects.filter(category=category, status='published')
    
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/posts_by_category.html', context)

def posts_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts_list = Post.objects.filter(tags=tag, status='published')
    
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'blog/posts_by_tag.html', context)

@login_required
@user_passes_test(is_author)
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many data for tags
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    context = {'form': form}
    return render(request, 'blog/post_form.html', context)

@login_required
@user_passes_test(is_author)
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    context = {'form': form, 'post': post}
    return render(request, 'blog/post_form.html', context)

@login_required
@user_passes_test(is_author)
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('home')
    
    context = {'post': post}
    return render(request, 'blog/post_confirm_delete.html', context)

@login_required
def dashboard(request):
    # Check if user is author or staff
    is_author_user = request.user.groups.filter(name='Authors').exists() or request.user.is_staff
    
    if is_author_user:
        user_posts = Post.objects.filter(author=request.user)
        published_posts = user_posts.filter(status='published')
        draft_posts = user_posts.filter(status='draft')
        user_comments = Comment.objects.filter(user=request.user)
        
        context = {
            'user_posts': user_posts,
            'published_posts': published_posts,
            'draft_posts': draft_posts,
            'total_posts': user_posts.count(),
            'user_comments': user_comments,
        }
        return render(request, 'blog/dashboard.html', context)
    else:
        # Reader dashboard
        user_comments = Comment.objects.filter(user=request.user)
        context = {
            'user_comments': user_comments,
        }
        return render(request, 'blog/dashboard.html', context)