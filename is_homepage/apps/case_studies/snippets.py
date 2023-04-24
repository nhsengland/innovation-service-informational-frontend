from django.db import models
from django_extensions.db.fields import AutoSlugField

from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class CaseStudiesTypeSnippet(models.Model):

    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', editable=True, help_text='A slug to identify case studies by this type')

    panels = [
        FieldPanel('title'),
        FieldPanel('slug')
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Case studies type'
        verbose_name_plural = 'Case studies types'
        ordering = ['title']
