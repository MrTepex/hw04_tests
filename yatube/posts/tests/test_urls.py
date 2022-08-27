from django.test import TestCase, Client

from ..models import Group, Post, User


class PostsURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Anne_Hathaway')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Описание'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_posts_urls_exists_at_desired_location_for_everybody(self):
        """Проверка отклика страниц приложения posts"""
        urls = {
            '/': 200,
            '/group/test_slug/': 200,
            '/profile/Anne_Hathaway/': 200,
            '/posts/1/': 200,
            '/posts/1/edit/': 302,
            '/create/': 302,
            '/unexisting_page/': 404,
        }
        for address, status in urls.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, status)

    def test_posts_create_url_redirect_anonymous_on_login(self):
        """Проверка редиректа неавторизованного пользователя
        со страницы создания поста на страницу "войти" """
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_posts_edit_url_redirect_anonymous_on_login(self):
        """Проверка редиректа неавторизованного пользователя
        со страницы изменения поста на страницу "войти" """
        response = self.guest_client.get('/posts/1/edit/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/posts/1/edit/')

    def test_posts_urls_uses_correct_templates(self):
        """Проверка на правильные шаблоны для страниц приложения users"""
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/test_slug/': 'posts/group_list.html',
            '/profile/Anne_Hathaway/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/posts/1/edit/': 'posts/post_create.html',
            '/create/': 'posts/post_create.html'
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
