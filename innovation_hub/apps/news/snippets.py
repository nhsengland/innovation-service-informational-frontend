from django.db import models

from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel


@register_snippet
class NewsTypeSnippet(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify news by this type'
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'News type'
        verbose_name_plural = 'News types'
        ordering = ['name']
