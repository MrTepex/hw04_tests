from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Group, Post


class PostFormsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = get_user_model().objects.create_user(username='Anne')
        cls.user_2 = get_user_model().objects.create_user(username='RandomMan')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user_1,
            text='Тестовый пост',
            group=cls.group,
        )
        cls.form = PostForm()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client_1 = Client()
        self.authorized_client_1.force_login(self.user_1)
        self.authorized_client_2 = Client()
        self.authorized_client_2.force_login(self.user_2)

    def test_post_create_form(self):
        """Проверка работы редиректа, создания поста
         и наличия новой записи после ее создания """
        posts_amount = Post.objects.count()
        form_data = {
            'text': 'Содержание только что созданного поста',
            'group': self.group.id,
        }
        response = self.authorized_client_1.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.post.author}))
        self.assertEqual(Post.objects.count(), posts_amount + 1)
        self.assertTrue(Post.objects.filter(
            text='Содержание только что созданного поста',
            group=self.group,
        ).exists())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_form_redirects_anonymous_to_login(self):
        posts_amount = Post.objects.count()
        response = self.guest_client.post(reverse('posts:post_create'))
        self.assertRedirects(response, f"{reverse('users:login')}?next="
                                       f"{reverse('posts:post_create')}")
        self.assertNotEqual(Post.objects.count(), posts_amount + 1)

    def test_post_edit_form(self):
        """Проверка работы PostForm при изменении текста в post_edit
        плюс редирект пользователя, который не авторизован
        или не является автором поста"""
        post = Post.objects.create(
            text='Старый текст',
            author=self.user_1
        )
        self.authorized_client_1.post(reverse(
            'posts:post_edit', kwargs={'post_id': post.id}),
            data={'text': 'Новый текст'},
            follow=True
        )
        self.assertEqual(Post.objects.get(id=post.id).text, 'Новый текст')
        self.assertRedirects(self.guest_client.get(
            reverse('posts:post_edit', kwargs={'post_id': 1})),
            f"{reverse('users:login')}?next="
            f"{reverse('posts:post_edit', kwargs={'post_id': 1})}")
        response = self.authorized_client_2.post(reverse(
            'posts:post_edit', kwargs={'post_id': post.id}),
            data={'text': 'Новый текст'},
            follow=True
        )
        self.assertRedirects(response, reverse('posts:post_detail',
                                               kwargs={'post_id': post.id}))

    def test_labels_and_help_texts(self):
        """Проверка labels и help_texts формы PostForm"""
        text_label = PostFormsTest.form.fields['text'].label
        text_help_text = PostFormsTest.form.fields['text'].help_text
        group_label = PostFormsTest.form.fields['group'].label
        group_help_text = PostFormsTest.form.fields['group'].help_text
        self.assertEqual(text_label, 'Содержание поста')
        self.assertEqual(text_help_text, 'Текст поста')
        self.assertEqual(group_label, 'Группа')
        self.assertEqual(
            group_help_text, 'Группа, к которой будет относиться пост')
