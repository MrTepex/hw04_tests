from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    """Модель для сообществ (групп)
        атрибуты:
         1. Название сообщества
         2. Адрес (относительный URL)
         3. Описание
         """
    title = models.CharField(max_length=200,
                             verbose_name='Заголовок вкладки')
    slug = models.SlugField(unique=True,
                            verbose_name='Относительный адрес')
    description = models.TextField(max_length=700,
                                   verbose_name='Описание группы')

    def __str__(self):
        return self.title


class Post(models.Model):
    """Модель для создания постов
    атрибуты:
     1. Содержание поста
     2. Дата и время публикации
     3. Автор поста
     4. Группа, к которой относится пост
     """
    text = models.TextField(verbose_name='Содержание поста')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата и время поста')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts',
                               verbose_name='Автор')
    group = models.ForeignKey(Group,
                              on_delete=models.SET_NULL,
                              related_name='posts',
                              verbose_name='Группа',
                              blank=True,
                              null=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]