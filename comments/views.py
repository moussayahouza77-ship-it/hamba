from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Like, Comment
from posts.models import Post


@require_POST
@login_required
def like_toggle(request):
    """Toggle like for a post or comment.
    Expects either 'post_id' or 'comment_id' in POST data.
    Returns JSON: { 'liked': bool, 'count': int }
    """
    user = request.user
    post_id = request.POST.get('post_id')
    comment_id = request.POST.get('comment_id')

    if post_id:
        post = get_object_or_404(Post, pk=post_id)
        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            # user already liked -> remove
            like.delete()
            liked = False
        else:
            liked = True
        count = Like.objects.filter(post=post).count()
        return JsonResponse({'liked': liked, 'count': count})

    if comment_id:
        comment = get_object_or_404(Comment, pk=comment_id)
        like, created = Like.objects.get_or_create(user=user, comment=comment)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        count = Like.objects.filter(comment=comment).count()
        return JsonResponse({'liked': liked, 'count': count})

    return JsonResponse({'error': 'invalid_target'}, status=400)
