# Generated by Django 4.1.6 on 2023-02-02 17:19

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.blocks
import wagtail.contrib.typed_table_block.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail_pdf_view.mixins
import wagtailmetadata.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0078_referenceindex'),
        ('taggit', '0005_auto_20220424_2025'),
        ('wagtailimages', '0024_index_image_file_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='InnovationPathwayDetailPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('content', wagtail.fields.StreamField([('inset_text', wagtail.blocks.StructBlock([('body', wagtail.blocks.RichTextBlock(required=True))], group='Text', icon='indent', label='Inset text', label_format='Inset text: {body}')), ('rich_text', wagtail.blocks.RichTextBlock(group='Text')), ('action_link', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(label='Link text', required=True)), ('external_url', wagtail.blocks.URLBlock(label='URL', required=False)), ('new_window', wagtail.blocks.BooleanBlock(label='Open in new window', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(label='Internal Page', required=False))], group='Buttons and Links', label='Action link', label_format='Action link: {text}')), ('button_link', wagtail.blocks.StructBlock([('link_label', wagtail.blocks.CharBlock(label='Label', required=True)), ('link_page', wagtail.blocks.PageChooserBlock(label='Internal page', required=False)), ('link_url', wagtail.blocks.URLBlock(label='External url', required=False))], group='Buttons and Links')), ('table', wagtail.contrib.typed_table_block.blocks.TypedTableBlock([('rich_text', wagtail.blocks.RichTextBlock())], group='Components')), ('card_group', wagtail.blocks.StructBlock([('column', wagtail.blocks.ChoiceBlock(choices=[('', 'Full-width'), ('one-half', 'One-half'), ('one-third', 'One-third')], required=False)), ('body', wagtail.blocks.StreamBlock([('card_basic', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False))])), ('card_clickable', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(help_text='Interal Page Link for the card', label='Internal Page', required=False)), ('url', wagtail.blocks.URLBlock(help_text='External Link for the card', label='URL', required=False))])), ('card_image', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('content_image', wagtail.images.blocks.ImageChooserBlock(label='Image', required=True)), ('alt_text', wagtail.blocks.CharBlock(required=True)), ('url', wagtail.blocks.URLBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='URL', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='Internal Page', required=False))])), ('card_feature', wagtail.blocks.StructBlock([('feature_heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=True))]))], required=True))], group='Components', icon='rectangle-list-regular', label='Cards', label_format='Cards')), ('icon_text_card_group', wagtail.blocks.StructBlock([('column', wagtail.blocks.ChoiceBlock(choices=[('full', 'Full width'), ('one-half', 'One half'), ('one-third', 'One third')])), ('cards', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('icon', wagtail.blocks.ChoiceBlock(choices=[('success', 'Success icon'), ('error', 'Error icon')], required=False)), ('text', wagtail.blocks.TextBlock(required=True))], icon='square-check-regular', label='Card', label_format='Card: {text}')))], group='Components')), ('vertical_stepper', wagtail.blocks.StructBlock([('steps', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=100, required=True)), ('text', wagtail.blocks.TextBlock(required=True))], icon='list-check', label='Step', label_format='Step: {title}')))], group='Components')), ('banner', wagtail.blocks.StructBlock([('background_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.blocks.CharBlock(label='Title', required=True)), ('supporting_text', wagtail.blocks.CharBlock(label='Supporting text', required=False)), ('link_label', wagtail.blocks.CharBlock(label='Call to action label', required=False)), ('link_page', wagtail.blocks.PageChooserBlock(label='Call to action page', required=False)), ('link_url', wagtail.blocks.URLBlock(label='Call to action url', required=False)), ('banner_height', wagtail.blocks.IntegerBlock(help_text='Choose a numeric value in pixels. If empty, height will default to the chosen image height', required=False)), ('layout', wagtail.blocks.ChoiceBlock(choices=[('title-text', 'Title - Text'), ('text-title', 'Text - Title')])), ('alignment', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center')]))], group='Images')), ('image_gallery', wagtail.blocks.StructBlock([('columns', wagtail.blocks.ChoiceBlock(choices=[(2, 2), (3, 3), (4, 4)], help_text='Choose the number of columns to show on each row (when viewing in desktop size.')), ('row_height', wagtail.blocks.IntegerBlock(help_text='Choose a numeric value in pixels.', required=False)), ('gallery', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('column_span', wagtail.blocks.ChoiceBlock(choices=[(1, 1), (2, 2), (3, 3), (4, 4)])), ('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('url', wagtail.blocks.URLBlock(required=False))])))], group='Images'))], blank=True, null=True, use_json_field=True)),
                ('search_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Search image')),
            ],
            options={
                'verbose_name': 'Innovation pathway detail page',
                'verbose_name_plural': 'Innovation pathway detail pages',
            },
            bases=(wagtail_pdf_view.mixins.PdfViewPageMixin, wagtailmetadata.models.WagtailImageMetadataMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='InnovationPathwayStagePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('content', wagtail.fields.StreamField([('inset_text', wagtail.blocks.StructBlock([('body', wagtail.blocks.RichTextBlock(required=True))], group='Text', icon='indent', label='Inset text', label_format='Inset text: {body}')), ('rich_text', wagtail.blocks.RichTextBlock(group='Text')), ('action_link', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(label='Link text', required=True)), ('external_url', wagtail.blocks.URLBlock(label='URL', required=False)), ('new_window', wagtail.blocks.BooleanBlock(label='Open in new window', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(label='Internal Page', required=False))], group='Buttons and Links', label='Action link', label_format='Action link: {text}')), ('button_link', wagtail.blocks.StructBlock([('link_label', wagtail.blocks.CharBlock(label='Label', required=True)), ('link_page', wagtail.blocks.PageChooserBlock(label='Internal page', required=False)), ('link_url', wagtail.blocks.URLBlock(label='External url', required=False))], group='Buttons and Links')), ('table', wagtail.contrib.typed_table_block.blocks.TypedTableBlock([('rich_text', wagtail.blocks.RichTextBlock())], group='Components')), ('card_group', wagtail.blocks.StructBlock([('column', wagtail.blocks.ChoiceBlock(choices=[('', 'Full-width'), ('one-half', 'One-half'), ('one-third', 'One-third')], required=False)), ('body', wagtail.blocks.StreamBlock([('card_basic', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False))])), ('card_clickable', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(help_text='Interal Page Link for the card', label='Internal Page', required=False)), ('url', wagtail.blocks.URLBlock(help_text='External Link for the card', label='URL', required=False))])), ('card_image', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('content_image', wagtail.images.blocks.ImageChooserBlock(label='Image', required=True)), ('alt_text', wagtail.blocks.CharBlock(required=True)), ('url', wagtail.blocks.URLBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='URL', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='Internal Page', required=False))])), ('card_feature', wagtail.blocks.StructBlock([('feature_heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=True))]))], required=True))], group='Components', icon='rectangle-list-regular', label='Cards', label_format='Cards')), ('icon_text_card_group', wagtail.blocks.StructBlock([('column', wagtail.blocks.ChoiceBlock(choices=[('full', 'Full width'), ('one-half', 'One half'), ('one-third', 'One third')])), ('cards', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('icon', wagtail.blocks.ChoiceBlock(choices=[('success', 'Success icon'), ('error', 'Error icon')], required=False)), ('text', wagtail.blocks.TextBlock(required=True))], icon='square-check-regular', label='Card', label_format='Card: {text}')))], group='Components')), ('vertical_stepper', wagtail.blocks.StructBlock([('steps', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=100, required=True)), ('text', wagtail.blocks.TextBlock(required=True))], icon='list-check', label='Step', label_format='Step: {title}')))], group='Components')), ('banner', wagtail.blocks.StructBlock([('background_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.blocks.CharBlock(label='Title', required=True)), ('supporting_text', wagtail.blocks.CharBlock(label='Supporting text', required=False)), ('link_label', wagtail.blocks.CharBlock(label='Call to action label', required=False)), ('link_page', wagtail.blocks.PageChooserBlock(label='Call to action page', required=False)), ('link_url', wagtail.blocks.URLBlock(label='Call to action url', required=False)), ('banner_height', wagtail.blocks.IntegerBlock(help_text='Choose a numeric value in pixels. If empty, height will default to the chosen image height', required=False)), ('layout', wagtail.blocks.ChoiceBlock(choices=[('title-text', 'Title - Text'), ('text-title', 'Text - Title')])), ('alignment', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center')]))], group='Images')), ('image_gallery', wagtail.blocks.StructBlock([('columns', wagtail.blocks.ChoiceBlock(choices=[(2, 2), (3, 3), (4, 4)], help_text='Choose the number of columns to show on each row (when viewing in desktop size.')), ('row_height', wagtail.blocks.IntegerBlock(help_text='Choose a numeric value in pixels.', required=False)), ('gallery', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('column_span', wagtail.blocks.ChoiceBlock(choices=[(1, 1), (2, 2), (3, 3), (4, 4)])), ('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('url', wagtail.blocks.URLBlock(required=False))])))], group='Images'))], blank=True, null=True, use_json_field=True)),
                ('search_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Search image')),
            ],
            options={
                'verbose_name': 'Innovation pathway stage page',
                'verbose_name_plural': 'Innovation pathway stages page',
            },
            bases=(wagtail_pdf_view.mixins.PdfViewPageMixin, wagtailmetadata.models.WagtailImageMetadataMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='InnovationPathwayStageSnippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sort_order', models.PositiveIntegerField(default=1)),
            ],
            options={
                'verbose_name': 'Innovation pathway stage',
                'verbose_name_plural': 'Innovation pathway stages',
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='InnovationPathwayStagePageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='innovation_pathway.innovationpathwaystagepage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='innovationpathwaystagepage',
            name='stage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='innovation_pathway.innovationpathwaystagesnippet'),
        ),
        migrations.AddField(
            model_name='innovationpathwaystagepage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='innovation_pathway.InnovationPathwayStagePageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='InnovationPathwayIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', wagtail.fields.RichTextField(blank=True, help_text='Introduction text that appears before stages list', verbose_name='Introduction')),
                ('content', wagtail.fields.StreamField([('inset_text', wagtail.blocks.StructBlock([('body', wagtail.blocks.RichTextBlock(required=True))], group='Text', icon='indent', label='Inset text', label_format='Inset text: {body}')), ('rich_text', wagtail.blocks.RichTextBlock(group='Text')), ('action_link', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(label='Link text', required=True)), ('external_url', wagtail.blocks.URLBlock(label='URL', required=False)), ('new_window', wagtail.blocks.BooleanBlock(label='Open in new window', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(label='Internal Page', required=False))], group='Buttons and Links', label='Action link', label_format='Action link: {text}')), ('button_link', wagtail.blocks.StructBlock([('link_label', wagtail.blocks.CharBlock(label='Label', required=True)), ('link_page', wagtail.blocks.PageChooserBlock(label='Internal page', required=False)), ('link_url', wagtail.blocks.URLBlock(label='External url', required=False))], group='Buttons and Links')), ('table', wagtail.contrib.typed_table_block.blocks.TypedTableBlock([('rich_text', wagtail.blocks.RichTextBlock())], group='Components')), ('card_group', wagtail.blocks.StructBlock([('column', wagtail.blocks.ChoiceBlock(choices=[('', 'Full-width'), ('one-half', 'One-half'), ('one-third', 'One-third')], required=False)), ('body', wagtail.blocks.StreamBlock([('card_basic', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False))])), ('card_clickable', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(help_text='Interal Page Link for the card', label='Internal Page', required=False)), ('url', wagtail.blocks.URLBlock(help_text='External Link for the card', label='URL', required=False))])), ('card_image', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('content_image', wagtail.images.blocks.ImageChooserBlock(label='Image', required=True)), ('alt_text', wagtail.blocks.CharBlock(required=True)), ('url', wagtail.blocks.URLBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='URL', required=False)), ('internal_page', wagtail.blocks.PageChooserBlock(help_text='Optional, if there is a link the entire card will be clickable.', label='Internal Page', required=False))])), ('card_feature', wagtail.blocks.StructBlock([('feature_heading', wagtail.blocks.CharBlock(required=True)), ('heading_level', wagtail.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Ignore this if there is no label. Default=3, Min=2, Max=6.', max_value=6, min_value=2)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('', 'Default'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], help_text="The heading size affects the visual size, this follows the front-end library's sizing.", required=False)), ('body', wagtail.blocks.RichTextBlock(required=True))]))], required=True))], group='Components', icon='rectangle-list-regular', label='Cards', label_format='Cards')), ('icon_text_card_group', wagtail.blocks.StructBlock([('column', wagtail.blocks.ChoiceBlock(choices=[('full', 'Full width'), ('one-half', 'One half'), ('one-third', 'One third')])), ('cards', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('icon', wagtail.blocks.ChoiceBlock(choices=[('success', 'Success icon'), ('error', 'Error icon')], required=False)), ('text', wagtail.blocks.TextBlock(required=True))], icon='square-check-regular', label='Card', label_format='Card: {text}')))], group='Components')), ('vertical_stepper', wagtail.blocks.StructBlock([('steps', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=100, required=True)), ('text', wagtail.blocks.TextBlock(required=True))], icon='list-check', label='Step', label_format='Step: {title}')))], group='Components')), ('banner', wagtail.blocks.StructBlock([('background_image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.blocks.CharBlock(label='Title', required=True)), ('supporting_text', wagtail.blocks.CharBlock(label='Supporting text', required=False)), ('link_label', wagtail.blocks.CharBlock(label='Call to action label', required=False)), ('link_page', wagtail.blocks.PageChooserBlock(label='Call to action page', required=False)), ('link_url', wagtail.blocks.URLBlock(label='Call to action url', required=False)), ('banner_height', wagtail.blocks.IntegerBlock(help_text='Choose a numeric value in pixels. If empty, height will default to the chosen image height', required=False)), ('layout', wagtail.blocks.ChoiceBlock(choices=[('title-text', 'Title - Text'), ('text-title', 'Text - Title')])), ('alignment', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center')]))], group='Images')), ('image_gallery', wagtail.blocks.StructBlock([('columns', wagtail.blocks.ChoiceBlock(choices=[(2, 2), (3, 3), (4, 4)], help_text='Choose the number of columns to show on each row (when viewing in desktop size.')), ('row_height', wagtail.blocks.IntegerBlock(help_text='Choose a numeric value in pixels.', required=False)), ('gallery', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('column_span', wagtail.blocks.ChoiceBlock(choices=[(1, 1), (2, 2), (3, 3), (4, 4)])), ('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('url', wagtail.blocks.URLBlock(required=False))])))], group='Images'))], blank=True, help_text='This content appears after stages list', null=True, use_json_field=True)),
                ('search_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Search image')),
            ],
            options={
                'verbose_name': 'Innovation pathway index page',
                'verbose_name_plural': 'Innovation pathway index page',
            },
            bases=(wagtail_pdf_view.mixins.PdfViewPageMixin, wagtailmetadata.models.WagtailImageMetadataMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='InnovationPathwayDetailPageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='innovation_pathway.innovationpathwaydetailpage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='innovationpathwaydetailpage',
            name='stage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='innovation_pathway.innovationpathwaystagesnippet'),
        ),
        migrations.AddField(
            model_name='innovationpathwaydetailpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='innovation_pathway.InnovationPathwayDetailPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
