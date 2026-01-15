from django.test import TestCase
from django.contrib.auth import get_user_model
from posts.models import Post
from .models import Comment


class CommentModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('u2', 'u2@example.com', 'pass')
        self.post = Post.objects.create(auteur=self.user, titre='T', contenu='C')

    def test_comment_create(self):
        c = Comment.objects.create(auteur=self.user, post=self.post, contenu='ok')
        self.assertEqual(c.contenu, 'ok')
