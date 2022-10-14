from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Post, Group


class StaticURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()



    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)


User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.user = User.objects.create_user(username='yaAdmin')
        self.group = Group.objects.create(
            title='Тестовая группа',
            slug='group_1',
            description='Тестовое описание',
        )
        self.post = Post.objects.create(
            author=self.user,
            text='Тестовый пост',
            group=self.group
        )


    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        test_author = PostURLTests.user
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(test_author)


    def test_urls_uses_correct_template_unauthorized_user(self):
        """URL-адрес использует соответствующий шаблон (незарегистрированный пользователь)"""
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': f'/group/{self.group.slug}/',
            'posts/profile.html': f'/profile/{self.post.author}/',
            'posts/post_detail.html': f'/posts/{self.post.pk}/'
        }

        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_uses_correct_template_logged_in_user(self):
        """URL-адрес использует соответствующий шаблон (зарегистрированный пользователь)"""
        templates_url_names = {
            '/create/': 'posts/create_post.html',
            f'/posts/{self.post.pk}/edit/': 'posts/create_post.html'
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client_author.get(address)
                self.assertTemplateUsed(response, template)