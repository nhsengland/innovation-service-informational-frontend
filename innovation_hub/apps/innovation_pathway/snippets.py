from django.db import models

from wagtail.snippets.models import register_snippet

# from wagtail.search import index


@register_snippet
class InnovationPathwayStageSnippet(models.Model):

    name = models.CharField(max_length=100)
    # sort_order = models.PositiveIntegerField()

    # class Category(index.Indexed, models.Mode):
    # search_fields = [index.SearchField('text', partial_match=True)]

    class Meta:
        verbose_name = 'Innovation pathway stage'
        verbose_name_plural = 'Innovation pathway stages'
        ordering = ['name']

    def __str__(self):
        return self.name
