from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class UsersURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()
        self.user = get_user_model().objects.create_user(
            username='Anne_Hathaway')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_users_urls_exist_at_desired_locations(self):
        """Проверка отклика страниц приложения users"""
        urls = {
            '/auth/logout/': HTTPStatus.OK,
            '/auth/signup/': HTTPStatus.OK,
            '/auth/login/': HTTPStatus.OK,
            '/auth/password_change/': HTTPStatus.FOUND,
            '/auth/password_change/done/': HTTPStatus.FOUND,
            '/auth/password_reset/': HTTPStatus.OK,
            '/auth/password_reset/done/': HTTPStatus.OK,
            '/auth/reset/1/2/': HTTPStatus.OK,
            '/auth/reset/done/': HTTPStatus.OK,
        }
        for address, status in urls.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, status)

    def test_users_pw_change_url_redirect_anonymous_on_login(self):
        """Проверка редиректа неавторизованного пользователя
        со страницы password_change на страницу "войти" """
        response = self.guest_client.get('/auth/password_change/',
                                         follow=True)
        self.assertRedirects(response, '/auth/login/?next=/auth/'
                                       'password_change/')

    def test_user_pw_change_done_url_redirect_anonymous_on_login(self):
        """Проверка редиректа неавторизованного пользователя
        со страницы password_change/done на страницу "войти" """
        response = self.guest_client.get('/auth/password_change/done/',
                                         follow=True)
        self.assertRedirects(response, '/auth/login/?next=/auth/'
                                       'password_change/done/')
