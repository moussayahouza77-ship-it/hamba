from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.db.models import Q
from comments.models import Comment, Like
from comments.forms import CommentForm
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.contrib import messages
from django.http import HttpResponseForbidden


def post_list(request):
    qs = Post.objects.filter(actif=True).select_related('auteur')
    paginator = Paginator(qs, 8)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'posts/post_list.html', {'posts': posts})


def post_search(request):
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    qs = Post.objects.filter(actif=True)
    if q:
        qs = qs.filter(models.Q(titre__icontains=q) | models.Q(contenu__icontains=q))
    if category:
        qs = qs.filter(categorie=category)
    qs = qs.select_related('auteur')
    paginator = Paginator(qs, 12)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'posts/post_list.html', {'posts': posts, 'search_query': q, 'search_category': category})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, actif=True)
    comments = Comment.objects.filter(post=post, parent__isnull=True).order_by('date_creation').select_related('auteur')
    # compute liked state for the current user
    post_liked = False
    comment_liked_ids = []
    if request.user.is_authenticated:
        post_liked = Like.objects.filter(user=request.user, post=post).exists()
        comment_ids = [c.pk for c in comments]
        likes = Like.objects.filter(user=request.user, comment_id__in=comment_ids).values_list('comment_id', flat=True)
        comment_liked_ids = list(likes)
    if request.method == 'POST':
        # basic throttling: prevent rapid comments
        from django.core.cache import cache
        if request.user.is_authenticated:
            key = f'comment_throttle_{request.user.pk}'
            last = cache.get(key)
            if last:
                messages.warning(request, 'Vous commentez trop rapidement. Attendez quelques secondes.')
                return redirect('posts:detail', pk=post.pk)
            cache.set(key, True, 5)  # 5 seconds throttle

        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.auteur = request.user
            comment.post = post
            parent_id = request.POST.get('parent')
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(pk=int(parent_id))
                    comment.parent = parent_comment
                except Comment.DoesNotExist:
                    pass
            comment.save()
            return redirect('posts:detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments, 'form': form, 'post_liked': post_liked, 'comment_liked_ids': comment_liked_ids})


@login_required
def post_create(request):
    # Only staff or superuser can create posts via site
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden('Permission denied')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.auteur = request.user
            post.save()
            messages.success(request, 'Publication créée.')
            return redirect('posts:detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form, 'create': True})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not (request.user == post.auteur or request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden('Permission denied')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Publication mise à jour.')
            return redirect('posts:detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form, 'create': False, 'post': post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not (request.user == post.auteur or request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden('Permission denied')
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Publication supprimée.')
        return redirect('posts:list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})
