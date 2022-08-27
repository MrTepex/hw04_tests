from django.test import TestCase, Client
from django.urls import reverse


class AboutTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_about_urls_exist_at_desired_location(self):
        urls = {
            '/about/author/': 200,
            '/about/tech/': 200,
        }
        for address, status in urls.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, status)

    def test_about_urls_uses_correct_templates(self):
        templates_url_names = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_about_author_page_uses_correct_template(self):
        response = self.guest_client.get(reverse('about:author'))
        self.assertTemplateUsed(response, 'about/author.html')
