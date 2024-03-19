from django.templatetags.static import static
from django.utils.html import format_html

from wagtail import hooks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import FieldPanel

from taggit.models import Tag


class AdminTagsSnippetViewSet(SnippetViewSet):
    Tag.panels = [FieldPanel('name'), FieldPanel('slug')]
    model = Tag
    menu_label = 'Tags'
    add_to_admin_menu = True
    icon = 'tag'
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    list_display = ['name', 'slug']
    search_fields = ['name']


register_snippet(AdminTagsSnippetViewSet)


@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static('css/wagtail_admin.css'))


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
