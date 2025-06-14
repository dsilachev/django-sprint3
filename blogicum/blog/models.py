from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

MAX_LENGTH_TITLE = 256


class PublishedModel(models.Model):
    is_published = models.BooleanField(
        _('Опубликовано'),
        default=True,
        help_text=_('Снимите галочку, чтобы скрыть публикацию.')
    )
    created_at = models.DateTimeField(_('Добавлено'), auto_now_add=True)

    class Meta:
        abstract = True


class Category(PublishedModel):
    title = models.CharField(_('Заголовок'), max_length=MAX_LENGTH_TITLE)
    description = models.TextField(_('Описание'))
    slug = models.SlugField(
        _('Идентификатор'),
        unique=True,
        help_text=_(
            'Идентификатор страницы для URL; разрешены символы латиницы, '
            'цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField(_('Название места'), max_length=MAX_LENGTH_TITLE)

    class Meta:
        verbose_name = _('местоположение')
        verbose_name_plural = _('Местоположения')

    def __str__(self):
        return self.name


class Post(PublishedModel):
    title = models.CharField(_('Заголовок'), max_length=MAX_LENGTH_TITLE)
    text = models.TextField(_('Текст'))
    pub_date = models.DateTimeField(
        _('Дата и время публикации'),
        help_text=_(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Автор публикации'),
        related_name='posts'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Местоположение'),
        related_name='posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Категория'),
        related_name='posts'
    )

    class Meta:
        verbose_name = _('публикация')
        verbose_name_plural = _('Публикации')
        ordering = ['-pub_date']

    def __str__(self):
        return self.title
