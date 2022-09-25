from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.text import slugify
import string
import random


class Author(models.Model):
    author = models.OneToOneField(User, verbose_name="имя автора", on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    otp = models.CharField(max_length=6, null=True,blank=True)

    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    def generate_code(self):
        random.seed()
        return str(random.randint(10000, 99999))

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.author.username

def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

class Category(models.Model):
    CATEGORY_CHOICES = (
        ('tank', 'Танк'),
        ('hils', 'Хилы'),
        ('dd', 'ДД'),
        ('merchant', 'Торговцы'),
        ('guildmaster', ' Гилдмастеры'),
        ('questgiver', 'Квестгиверы'),
        ('blacksmith', 'Кузнецы'),
        ('leatherworker', 'Кожевники'),
        ('potionMaster', 'Зельевары'),
        ('spellMaster', 'Мастера заклинаний'),
    )

    name = models.CharField(max_length=20,choices=CATEGORY_CHOICES,unique = True,default='танк', verbose_name='Категория')
    slug = models.SlugField(verbose_name='URLcom', null=True)



    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Post(models.Model):

    title = models.CharField(max_length=40, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержание')
    slug = models.SlugField(max_length=250,unique=True, db_index=True, verbose_name="URL")
    cat = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name="Категория")
    image = models.ImageField(blank=True, upload_to='project/%Y-%m-%d',null=True,default=None,
                              verbose_name='Изображение')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор объявления')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='Опубликовано')
    updated = models.DateTimeField(auto_now=True,verbose_name='Обновлено')
    is_published = models.BooleanField(default=True, verbose_name="Публикация")


    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-publish',]

    def __str__(self):
        return f"{self. author}:{self.title}"

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + self.title)
        super(Post, self).save(*args, **kwargs)

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post=self).count()


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',on_delete=models.CASCADE,)
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True,verbose_name="Автор комментария")
    email = models.EmailField()
    body = models.TextField(max_length=250,null=True,verbose_name="Текст комментария")
    created = models.DateTimeField(auto_now_add=True,verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False,verbose_name="Статус")

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.body, self.post)

