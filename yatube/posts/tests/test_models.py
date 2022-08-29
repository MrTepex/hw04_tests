from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post


class PostsModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(
            username='Anne_Hathaway'
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверка, что у моделей корректно работает __str__."""
        group = PostsModelTest.group
        post = PostsModelTest.post
        expected_group_name = group.title
        expected_post_text = post.text[:15]
        self.assertEqual(expected_group_name, str(group))
        self.assertEqual(expected_post_text, str(post))

    def test_post_model_verbose_name(self):
        """Проверка корректности verbose_name атрибутов модели"""
        post = PostsModelTest.post
        field_verboses = {
            'text': 'Содержание поста',
            'pub_date': 'Дата и время поста',
            'group': 'Группа',
            'author': 'Автор',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                post_verbose = post._meta.get_field(field).verbose_name
                self.assertEqual(post_verbose, expected_value,
                                 f'verbose_name для "{field}" модели '
                                 f'"{post.__class__.__name__}" некорректно')
