from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """Форма для создания новой записи"""
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'text': 'Содержание поста',
            'group': 'Группа'}
        help_texts = {
            'text': 'Текст поста',
            'group': 'Группа, к которой будет относиться пост',
        }
