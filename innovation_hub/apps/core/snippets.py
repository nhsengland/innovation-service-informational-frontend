from django.db import models

from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

# from wagtail.search import index


@register_snippet
class Category(models.Model):

    name = models.CharField(max_length=100)
    # sort_order = models.PositiveIntegerField()

    # class Category(index.Indexed, models.Mode):
    # search_fields = [index.SearchField('text', partial_match=True)]

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name
