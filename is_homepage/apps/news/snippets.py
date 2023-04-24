from django.db import models
from django_extensions.db.fields import AutoSlugField

from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class NewsTypeSnippet(models.Model):

    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', editable=True, help_text='A slug to identify news by this type')

    panels = [
        FieldPanel('title'),
        FieldPanel('slug')
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'News type'
        verbose_name_plural = 'News types'
        ordering = ['title']
