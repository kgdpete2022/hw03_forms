from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )


    def test_models_have_correct_object_names(self):
            """Проверяем, что у моделей корректно работает __str__."""
            
            group = PostModelTest.group
            expected_group_title = group.title
            real_group_title = group.title
            self.assertEqual(expected_group_title, str(real_group_title))

            post = PostModelTest.post
            expected_post_representation = post.text[:15]
            real_post_representation = post
            self.assertEqual(expected_post_representation, str(real_post_representation))
    