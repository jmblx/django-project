from django.db import models
from django.urls import reverse


# Create your models here.

class Memes(models.Model):
    '''Мемы с тачками'''
    objects = None
    name = models.CharField('Название мема', max_length=30)
    img = models.ImageField('Мем', upload_to='image/%Y')
    date = models.DateField('Дата')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT)
    author = models.CharField('Автор мема', max_length=30)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def get_absolute_url(self):
        return reverse('mem', kwargs={'mem_slug': self.slug})

    class Meta:
        verbose_name = 'Мемы'
        verbose_name_plural = 'Мемы'
        ordering = ['id']


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Comments(models.Model):
    '''Комментарии'''
    email = models.EmailField()
    name = models.CharField('Имя', max_length=50)
    text_comments = models.TextField('Текст комментария', max_length=1000)
    mem = models.ForeignKey(Memes, verbose_name='Мем', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.name}, {self.mem}'
