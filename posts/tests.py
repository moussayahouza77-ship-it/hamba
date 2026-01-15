from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post


class PostModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('u1', 'u1@example.com', 'pass')

    def test_create_post(self):
        p = Post.objects.create(auteur=self.user, titre='T1', contenu='C')
        self.assertEqual(str(p), 'T1')
        self.assertTrue(p.actif)
