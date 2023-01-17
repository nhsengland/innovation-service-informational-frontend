from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.admin.edit_handlers import FieldPanel

from taggit.models import Tag


class AdminTagsModel(ModelAdmin):
    Tag.panels = [FieldPanel('name'), FieldPanel('slug')]
    model = Tag
    menu_label = 'Tags'
    menu_icon = 'tag'
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    list_display = ['name', 'slug']
    search_fields = ['name']


modeladmin_register(AdminTagsModel)
