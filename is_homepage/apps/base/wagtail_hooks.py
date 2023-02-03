from django.utils.safestring import mark_safe

from wagtail import hooks
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


@hooks.register('register_icons')
def register_icons(icons):
    return icons + [
        'svg/columns_gap.svg',
        'svg/crown.svg',
        'svg/images.svg',
        'svg/indent.svg',
        'svg/layout_three_columns.svg',
        'svg/list_check.svg',
        'svg/rectangle_ad.svg',
        'svg/rectangle_list_regular.svg',
        'svg/square_arrow_up_right.svg',
        'svg/square_caret_right.svg',
        'svg/square_check_regular.svg',
        'svg/square_check_solid.svg',
    ]
