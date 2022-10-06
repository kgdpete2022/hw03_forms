from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField("Название группы", max_length=200)
    slug = models.SlugField("URL-адрес группы", max_length=200, unique=True)
    description = models.TextField("Описание группы")

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField("Текст публикации")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Автор публикации",
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name="Группа публикации"
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']
