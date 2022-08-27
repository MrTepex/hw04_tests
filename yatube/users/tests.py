from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

User = get_user_model()


class UsersURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Anne_Hathaway')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_users_urls_exist_at_desired_locations(self):
        """Проверка отклика страниц приложения users"""
        urls = {
            '/auth/logout/': 200,
            '/auth/signup/': 200,
            '/auth/login/': 200,
            '/auth/password_change/': 302,
            '/auth/password_change/done/': 302,
            '/auth/password_reset/': 200,
            '/auth/password_reset/done/': 200,
            '/auth/reset/1/2/': 200,
            '/auth/reset/done/': 200,
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

    def test_users_logout_url_uses_correct_template(self):
        """Проверка на правильный шаблон для страницы
         logout приложения users"""
        response = self.authorized_client.get('/auth/logout/')
        self.assertTemplateUsed(response, 'users/logged_out.html')

    def test_users_pages_uses_correct_templates(self):
        """Проверка на правильные шаблоны для страниц приложения users"""
        template_url_names = {
            '/auth/signup/': 'users/signup.html',
            '/auth/login/': 'users/login.html',
            '/auth/password_change/': 'users/password_change_form.html',
            '/auth/password_change/done/': 'users/password_change_done.html',
            '/auth/password_reset/': 'users/password_reset_form.html',
            '/auth/password_reset/done/': 'users/password_reset_done.html',
            '/auth/reset/1/2/': 'users/password_reset_confirm.html',
            '/auth/reset/done/': 'users/password_reset_complete.html',
        }
        for address, template in template_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template,
                                        f'\033[1m"{address}" не использует '
                                        f'"{template}"\033[0m')

    def test_signup_form_creates_new_user(self):
        """Проверка создания нового пользователя формой SignUp"""
        form_data = {
            'username': 'NewUser',
            'password1': 'QwErTy1234yTrEwQ',
            'password2': 'QwErTy1234yTrEwQ'
        }
        self.guest_client.post(reverse('users:signup'),
                               data=form_data,
                               follow=True
                               )
        self.assertTrue(User.objects.filter(username='NewUser').exists())
