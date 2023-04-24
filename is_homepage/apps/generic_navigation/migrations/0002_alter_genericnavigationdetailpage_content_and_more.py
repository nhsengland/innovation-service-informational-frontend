# Generated by Django 4.1.8 on 2023-04-24 11:54

from django.db import migrations
import wagtail.blocks
import wagtail.contrib.typed_table_block.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtailnhsukfrontend.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('generic_navigation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericnavigationdetailpage',
            name='content',
            field=wagtail.fields.StreamField([('layout_grid', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('column_width', wagtail.blocks.ChoiceBlock(choices=[('full', 'Full'), ('one-half', 'One half')], label='Width')), ('content', wagtail.blocks.StreamBlock([('card_group', wagtail.blocks.StructBlock([('column', wagtail.blocks.ChoiceBlock(choices=[('', 'Full-width'), ('one-half', 'One-half'), ('one-third', 'One-third')], required=False)), ('body', wagtail.blocks.StreamBlock([('card_basic', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False))])), ('card_clickable', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(help_text='Interal Page Link for the card', label='Internal Page', required=False)), ('url', wagtail.blocks.URLBlock(help_text='External Link for the card', label='URL', required=False))])), ('card_image', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('content_image', wagtail.images.blocks.ImageChooserBlock(label='Image', required=True)), ('alt_text', wagtail.blocks.CharBlock(required=True)), ('url', wagtail.blocks.URLBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='URL', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='Internal Page', required=False))])), ('card_feature', wagtail.blocks.StructBlock([('feature_heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=True))]))], required=True))], group='Components', icon='rectangle-list-regular', label='Cards', label_format='Cards')), ('collapsible_details', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=True)), ('content', wagtail.blocks.StreamBlock([('description_list', wagtail.blocks.StructBlock([('rows', wagtail.blocks.ListBlock(wagtailnhsukfrontend.blocks.SummaryListRowBlock)), ('no_border', wagtail.blocks.BooleanBlock(default=False, required=False))], group='Lists', label='Description list', label_format='Description list: {rows}')), ('table', wagtail.contrib.typed_table_block.blocks.TypedTableBlock([('rich_text', wagtail.blocks.RichTextBlock())], group='Lists')), ('action_link', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(label='Link text', required=True)), ('external_url', wagtail.blocks.URLBlock(label='URL', required=False)), ('new_window', wagtail.blocks.BooleanBlock(label='Open in new window', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(label='Internal Page', required=False))], group='Navigation', label='Action link', label_format='Action link: {text}')), ('inset_text', wagtail.blocks.StructBlock([('body', wagtail.blocks.RichTextBlock(required=True))], group='Text', icon='indent', label='Inset text', label_format='Inset text: {body}')), ('rich_text', wagtail.blocks.RichTextBlock(group='Text'))], required=True))], group='Components')), ('text_card_group', wagtail.blocks.StructBlock([('column_width', wagtail.blocks.ChoiceBlock(choices=[('full', 'Full'), ('one-half', 'One half'), ('one-third', 'One third')])), ('cards', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('icon', wagtail.blocks.ChoiceBlock(choices=[('success', 'Success icon'), ('error', 'Error icon'), ('bullet', 'Bullet icon')], required=False)), ('text', wagtail.blocks.TextBlock(required=True))], icon='square-check-regular', label='Card', label_format='Card: {text}')))], group='Components')), ('banner', wagtail.blocks.StructBlock([('background_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.blocks.CharBlock(label='Title', required=True)), ('supporting_text', wagtail.blocks.CharBlock(label='Supporting text', required=False)), ('link_label', wagtail.blocks.CharBlock(label='Call to action label', required=False)), ('link_page', wagtail.blocks.PageChooserBlock(label='Call to action page', required=False)), ('link_url', wagtail.blocks.URLBlock(label='Call to action url', required=False)), ('banner_height', wagtail.blocks.IntegerBlock(help_text='Choose a numeric value in pixels. If empty, height will default to the chosen image height', required=False)), ('layout', wagtail.blocks.ChoiceBlock(choices=[('title-text', 'Title - Text'), ('text-title', 'Text - Title')])), ('alignment', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center')]))], group='Images')), ('image_gallery', wagtail.blocks.StructBlock([('columns', wagtail.blocks.ChoiceBlock(choices=[(2, 2), (3, 3), (4, 4)], help_text='Choose the number of columns to show on each row (when viewing in desktop size.')), ('row_height', wagtail.blocks.IntegerBlock(help_text='Choose a numeric value in pixels.', required=False)), ('gallery', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('column_span', wagtail.blocks.ChoiceBlock(choices=[(1, 1), (2, 2), (3, 3), (4, 4)])), ('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('url', wagtail.blocks.URLBlock(required=False))])))], group='Images')), ('description_list', wagtail.blocks.StructBlock([('rows', wagtail.blocks.ListBlock(wagtailnhsukfrontend.blocks.SummaryListRowBlock)), ('no_border', wagtail.blocks.BooleanBlock(default=False, required=False))], group='Lists', label='Description list', label_format='Description list: {rows}')), ('table', wagtail.contrib.typed_table_block.blocks.TypedTableBlock([('rich_text', wagtail.blocks.RichTextBlock())], group='Lists')), ('vertical_stepper', wagtail.blocks.StructBlock([('steps', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=100, required=True)), ('text', wagtail.blocks.TextBlock(required=True))], icon='list-check', label='Step', label_format='Step: {title}')))], group='Lists')), ('action_link', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(label='Link text', required=True)), ('external_url', wagtail.blocks.URLBlock(label='URL', required=False)), ('new_window', wagtail.blocks.BooleanBlock(label='Open in new window', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(label='Internal Page', required=False))], group='Navigation', label='Action link', label_format='Action link: {text}')), ('button_link', wagtail.blocks.StructBlock([('link_label', wagtail.blocks.CharBlock(label='Label', required=True)), ('link_page', wagtail.blocks.PageChooserBlock(label='Internal page', required=False)), ('link_url', wagtail.blocks.URLBlock(label='External url', required=False))], group='Navigation')), ('inset_text', wagtail.blocks.StructBlock([('body', wagtail.blocks.RichTextBlock(required=True))], group='Text', icon='indent', label='Inset text', label_format='Inset text: {body}')), ('rich_text', wagtail.blocks.RichTextBlock(group='Text'))], blank=True, collapsed=True, null=True, use_json_field=True))], icon='square-check-regular', label='Column', label_format='Column: {column_width}'), group='Layout'))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='genericnavigationindexpage',
            name='content',
            field=wagtail.fields.StreamField([('layout_grid', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('column_width', wagtail.blocks.ChoiceBlock(choices=[('full', 'Full'), ('one-half', 'One half')], label='Width')), ('content', wagtail.blocks.StreamBlock([('card_group', wagtail.blocks.StructBlock([('column', wagtail.blocks.ChoiceBlock(choices=[('', 'Full-width'), ('one-half', 'One-half'), ('one-third', 'One-third')], required=False)), ('body', wagtail.blocks.StreamBlock([('card_basic', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False))])), ('card_clickable', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(help_text='Interal Page Link for the card', label='Internal Page', required=False)), ('url', wagtail.blocks.URLBlock(help_text='External Link for the card', label='URL', required=False))])), ('card_image', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('content_image', wagtail.images.blocks.ImageChooserBlock(label='Image', required=True)), ('alt_text', wagtail.blocks.CharBlock(required=True)), ('url', wagtail.blocks.URLBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='URL', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='Internal Page', required=False))])), ('card_feature', wagtail.blocks.StructBlock([('feature_heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=True))]))], required=True))], group='Components', icon='rectangle-list-regular', label='Cards', label_format='Cards')), ('collapsible_details', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=True)), ('content', wagtail.blocks.StreamBlock([('description_list', wagtail.blocks.StructBlock([('rows', wagtail.blocks.ListBlock(wagtailnhsukfrontend.blocks.SummaryListRowBlock)), ('no_border', wagtail.blocks.BooleanBlock(default=False, required=False))], group='Lists', label='Description list', label_format='Description list: {rows}')), ('table', wagtail.contrib.typed_table_block.blocks.TypedTableBlock([('rich_text', wagtail.blocks.RichTextBlock())], group='Lists')), ('action_link', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(label='Link text', required=True)), ('external_url', wagtail.blocks.URLBlock(label='URL', required=False)), ('new_window', wagtail.blocks.BooleanBlock(label='Open in new window', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(label='Internal Page', required=False))], group='Navigation', label='Action link', label_format='Action link: {text}')), ('inset_text', wagtail.blocks.StructBlock([('body', wagtail.blocks.RichTextBlock(required=True))], group='Text', icon='indent', label='Inset text', label_format='Inset text: {body}')), ('rich_text', wagtail.blocks.RichTextBlock(group='Text'))], required=True))], group='Components')), ('text_card_group', wagtail.blocks.StructBlock([('column_width', wagtail.blocks.ChoiceBlock(choices=[('full', 'Full'), ('one-half', 'One half'), ('one-third', 'One third')])), ('cards', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('icon', wagtail.blocks.ChoiceBlock(choices=[('success', 'Success icon'), ('error', 'Error icon'), ('bullet', 'Bullet icon')], required=False)), ('text', wagtail.blocks.TextBlock(required=True))], icon='square-check-regular', label='Card', label_format='Card: {text}')))], group='Components')), ('banner', wagtail.blocks.StructBlock([('background_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.blocks.CharBlock(label='Title', required=True)), ('supporting_text', wagtail.blocks.CharBlock(label='Supporting text', required=False)), ('link_label', wagtail.blocks.CharBlock(label='Call to action label', required=False)), ('link_page', wagtail.blocks.PageChooserBlock(label='Call to action page', required=False)), ('link_url', wagtail.blocks.URLBlock(label='Call to action url', required=False)), ('banner_height', wagtail.blocks.IntegerBlock(help_text='Choose a numeric value in pixels. If empty, height will default to the chosen image height', required=False)), ('layout', wagtail.blocks.ChoiceBlock(choices=[('title-text', 'Title - Text'), ('text-title', 'Text - Title')])), ('alignment', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center')]))], group='Images')), ('image_gallery', wagtail.blocks.StructBlock([('columns', wagtail.blocks.ChoiceBlock(choices=[(2, 2), (3, 3), (4, 4)], help_text='Choose the number of columns to show on each row (when viewing in desktop size.')), ('row_height', wagtail.blocks.IntegerBlock(help_text='Choose a numeric value in pixels.', required=False)), ('gallery', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('column_span', wagtail.blocks.ChoiceBlock(choices=[(1, 1), (2, 2), (3, 3), (4, 4)])), ('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('url', wagtail.blocks.URLBlock(required=False))])))], group='Images')), ('description_list', wagtail.blocks.StructBlock([('rows', wagtail.blocks.ListBlock(wagtailnhsukfrontend.blocks.SummaryListRowBlock)), ('no_border', wagtail.blocks.BooleanBlock(default=False, required=False))], group='Lists', label='Description list', label_format='Description list: {rows}')), ('table', wagtail.contrib.typed_table_block.blocks.TypedTableBlock([('rich_text', wagtail.blocks.RichTextBlock())], group='Lists')), ('vertical_stepper', wagtail.blocks.StructBlock([('steps', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=100, required=True)), ('text', wagtail.blocks.TextBlock(required=True))], icon='list-check', label='Step', label_format='Step: {title}')))], group='Lists')), ('action_link', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(label='Link text', required=True)), ('external_url', wagtail.blocks.URLBlock(label='URL', required=False)), ('new_window', wagtail.blocks.BooleanBlock(label='Open in new window', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(label='Internal Page', required=False))], group='Navigation', label='Action link', label_format='Action link: {text}')), ('button_link', wagtail.blocks.StructBlock([('link_label', wagtail.blocks.CharBlock(label='Label', required=True)), ('link_page', wagtail.blocks.PageChooserBlock(label='Internal page', required=False)), ('link_url', wagtail.blocks.URLBlock(label='External url', required=False))], group='Navigation')), ('inset_text', wagtail.blocks.StructBlock([('body', wagtail.blocks.RichTextBlock(required=True))], group='Text', icon='indent', label='Inset text', label_format='Inset text: {body}')), ('rich_text', wagtail.blocks.RichTextBlock(group='Text'))], blank=True, collapsed=True, null=True, use_json_field=True))], icon='square-check-regular', label='Column', label_format='Column: {column_width}'), group='Layout'))], blank=True, null=True, use_json_field=True),
        ),
    ]
