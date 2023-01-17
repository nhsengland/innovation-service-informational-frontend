from django.db import models

from wagtail.snippets.models import register_snippet

from wagtail.admin.panels import FieldPanel


@register_snippet
class InnovationPathwayStageSnippet(models.Model):

    name = models.CharField(max_length=100)
    sort_order = models.PositiveIntegerField(default=1)

    panels = [FieldPanel('name'), FieldPanel('sort_order')]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Innovation pathway stage'
        verbose_name_plural = 'Innovation pathway stages'
        ordering = ['sort_order']
