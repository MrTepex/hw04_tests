from django.test import TestCase, Client
from django.urls import reverse

from ..forms import PostForm
from ..models import Group, Post, User


class PostFormsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Anne')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
        )
        cls.form = PostForm()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_create_form(self):
        """Проверка работы редиректа, создания поста
         и наличия новой записи после ее создания """
        posts_amount = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.post.author})
                             )
        self.assertEqual(Post.objects.count(), posts_amount + 1)
        self.assertTrue(Post.objects.filter(
            text='Тестовый текст',
            group=self.group,
        ).exists()
                        )

    def test_post_edit_form(self):
        """Проверка работы PostForm при изменении текста в post_edit"""
        post = Post.objects.create(
            text='Старый текст',
            author=self.user
        )
        self.authorized_client.post(reverse(
            'posts:post_edit', kwargs={'post_id': post.id}),
            data={'text': 'Новый текст'},
            follow=True
        )
        self.assertEqual(Post.objects.get(id=post.id).text, 'Новый текст')

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
