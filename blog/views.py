from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.contrib import messages
from django.http import Http404, HttpResponseForbidden
from django.urls import reverse_lazy, reverse


from .models import Post, Category, Tag, Comment, PostLike
from .forms import RegisterForm, PostForm, CommentForm
from .decorators import author_required

User = get_user_model()


# -------------------------------------------------------------------
# Authentication Views
# -------------------------------------------------------------------

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Likhoni, {user.username}! Your account has been created.")
            return redirect('index')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        messages.info(request, "You have been logged out successfully.")
    return redirect('index')


# -------------------------------------------------------------------
# Public Listing & Search Views
# -------------------------------------------------------------------

def index_view(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    tag_slug = request.GET.get('tag', '').strip()

    posts = Post.objects.filter(status='PUBLISHED').select_related('category', 'author').prefetch_related('tags')

    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=active_category)

    active_tag = None
    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=active_tag)

    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()

    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        'page_obj': page_obj,
        'query': query,
        'categories': categories,
        'tags': tags,
        'active_category': active_category,
        'active_tag': active_tag,
    }
    return render(request, 'blog/index.html', context)


def category_posts_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(status='PUBLISHED', category=category).select_related('author').prefetch_related('tags')

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }
    return render(request, 'blog/category_posts.html', context)


def tag_posts_view(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(status='PUBLISHED', tags=tag).select_related('category', 'author').prefetch_related('tags')

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tag': tag,
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }
    return render(request, 'blog/tag_posts.html', context)


# -------------------------------------------------------------------
# Post Detail & Interactivity
# -------------------------------------------------------------------

def post_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Draft visibility check: Only author or admin can view draft
    if post.status == 'DRAFT':
        if not (request.user.is_authenticated and (request.user == post.author or request.user.is_superuser)):
            raise Http404("Post not found or unavailable.")

    # View count tracking per session to prevent double counting on simple refreshes
    session_key = 'viewed_posts'
    viewed_posts = request.session.get(session_key, [])
    if post.pk not in viewed_posts:
        post.view_count += 1
        post.save(update_fields=['view_count'])
        viewed_posts.append(post.pk)
        request.session[session_key] = viewed_posts
        request.session.modified = True

    # User like status
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = PostLike.objects.filter(post=post, user=request.user).exists()

    comments = post.comments.select_related('user').order_by('created_at')
    comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_has_liked': user_has_liked,
        'likes_count': post.likes.count(),
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def like_toggle_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like_obj, created = PostLike.objects.get_or_create(post=post, user=request.user)

    if not created:
        like_obj.delete()
        messages.info(request, "Unliked post.")
    else:
        messages.success(request, "Liked post!")

    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('post_detail', slug=post.slug)


@login_required
def comment_create_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, "Your comment has been published.")
        else:
            messages.error(request, "Comment could not be empty.")
    return redirect('post_detail', slug=post.slug)


@login_required
def comment_delete_view(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_slug = comment.post.slug

    # Moderation check: comment owner, post author, or superuser
    if request.user == comment.user or request.user == comment.post.author or request.user.is_superuser:
        comment.delete()
        messages.success(request, "Comment deleted.")
        return redirect('post_detail', slug=post_slug)
    else:
        messages.error(request, "You do not have permission to delete this comment.")
        raise PermissionDenied("You do not have permission to delete this comment.")


# -------------------------------------------------------------------
# Author Dashboard & Management
# -------------------------------------------------------------------

@author_required
def author_dashboard_view(request):
    posts = Post.objects.filter(author=request.user).select_related('category').prefetch_related('tags')
    
    total_posts = posts.count()
    published_count = posts.filter(status='PUBLISHED').count()
    draft_count = posts.filter(status='DRAFT').count()
    total_views = posts.aggregate(Sum('view_count'))['view_count__sum'] or 0

    context = {
        'posts': posts,
        'total_posts': total_posts,
        'published_count': published_count,
        'draft_count': draft_count,
        'total_views': total_views,
    }
    return render(request, 'blog/author_dashboard.html', context)


@author_required
def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, f"Post '{post.title}' created successfully!")
            return redirect('author_dashboard')
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Create New Blog Post'})


@author_required
def post_edit_view(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Ownership check: must be post author or superuser
    if not (post.author == request.user or request.user.is_superuser):
        messages.error(request, "You are not authorized to edit this post.")
        raise PermissionDenied("You are not authorized to edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            saved_post = form.save()
            messages.success(request, f"Post '{saved_post.title}' updated successfully!")
            return redirect('author_dashboard')
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {'form': form, 'post': post, 'title': f'Edit Post: {post.title}'})


@author_required
def post_delete_view(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Ownership check: must be post author or superuser
    if not (post.author == request.user or request.user.is_superuser):
        messages.error(request, "You are not authorized to delete this post.")
        raise PermissionDenied("You are not authorized to delete this post.")

    if request.method == 'POST':
        title = post.title
        post.delete()
        messages.success(request, f"Post '{title}' was deleted successfully.")
        return redirect('author_dashboard')

    return render(request, 'blog/post_confirm_delete.html', {'post': post})


def author_profile_view(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author, status='PUBLISHED').select_related('category').prefetch_related('tags')

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'author_profile': author,
        'page_obj': page_obj,
    }
    return render(request, 'blog/author_profile.html', context)


# -------------------------------------------------------------------
# Site Admin Dashboard & Management Views
# -------------------------------------------------------------------

from .decorators import admin_required
from .forms import CategoryForm, TagForm

@admin_required
def admin_dashboard_view(request):
    tab = request.GET.get('tab', 'overview')

    # Platform Analytics Metrics
    total_users = User.objects.count()
    authors_count = User.objects.filter(is_author=True).count()
    readers_count = User.objects.filter(is_author=False, is_superuser=False).count()
    
    all_posts = Post.objects.all().select_related('category', 'author').order_by('-created_at')
    total_posts = all_posts.count()
    published_posts_count = all_posts.filter(status='PUBLISHED').count()
    draft_posts_count = all_posts.filter(status='DRAFT').count()
    total_views = all_posts.aggregate(Sum('view_count'))['view_count__sum'] or 0

    all_users = User.objects.all().order_by('-date_joined')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    comments = Comment.objects.all().select_related('user', 'post').order_by('-created_at')

    category_form = CategoryForm()
    tag_form = TagForm()

    context = {
        'tab': tab,
        'total_users': total_users,
        'authors_count': authors_count,
        'readers_count': readers_count,
        'all_posts': all_posts,
        'total_posts': total_posts,
        'published_posts_count': published_posts_count,
        'draft_posts_count': draft_posts_count,
        'total_views': total_views,
        'all_users': all_users,
        'categories': categories,
        'tags': tags,
        'comments': comments,
        'category_form': category_form,
        'tag_form': tag_form,
    }
    return render(request, 'blog/admin_dashboard.html', context)


@admin_required
def admin_user_toggle_author_view(request, pk):
    target_user = get_object_or_404(User, pk=pk)
    target_user.is_author = not target_user.is_author
    target_user.save()
    status = "Author" if target_user.is_author else "Reader"
    messages.success(request, f"User '{target_user.username}' role updated to {status}.")
    return redirect(reverse('admin_dashboard') + '?tab=users')


@admin_required
def admin_post_toggle_status_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.status = 'DRAFT' if post.status == 'PUBLISHED' else 'PUBLISHED'
    post.save()
    messages.success(request, f"Post '{post.title}' status changed to {post.get_status_display()}.")
    return redirect(reverse('admin_dashboard') + '?tab=posts')


@admin_required
def admin_category_create_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Category '{category.name}' created successfully.")
        else:
            messages.error(request, "Failed to create category. Check input.")
    return redirect(reverse('admin_dashboard') + '?tab=categories')


@admin_required
def admin_category_edit_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Category '{category.name}' updated.")
            return redirect(reverse('admin_dashboard') + '?tab=categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'blog/admin_category_edit.html', {'form': form, 'category': category})


@admin_required
def admin_category_delete_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    name = category.name
    category.delete()
    messages.success(request, f"Category '{name}' deleted.")
    return redirect(reverse('admin_dashboard') + '?tab=categories')


@admin_required
def admin_tag_create_view(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            messages.success(request, f"Tag '{tag.name}' created.")
        else:
            messages.error(request, "Failed to create tag.")
    return redirect(reverse('admin_dashboard') + '?tab=tags')


@admin_required
def admin_tag_delete_view(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    name = tag.name
    tag.delete()
    messages.success(request, f"Tag '{name}' deleted.")
    return redirect(reverse('admin_dashboard') + '?tab=tags')

