# Generated by Django 4.1.6 on 2023-02-09 12:52

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0083_workflowcontenttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseNavigationSnippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, help_text='Unique identifier of the menu.', populate_from='title', verbose_name='Menu identifier')),
            ],
            options={
                'verbose_name': 'Navigation',
                'verbose_name_plural': 'Navigation',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='NavigationMenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('menu_title', models.CharField(max_length=50, null=True, verbose_name='Title')),
                ('menu_description', models.CharField(blank=True, help_text='Description is only visible within submenus', max_length=500, null=True, verbose_name='Description')),
                ('menu_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Url')),
                ('open_in_new_tab', models.BooleanField(blank=True, default=False, verbose_name='Open in a new tab?')),
                ('submenu', models.CharField(blank=True, help_text='Slug of the menu to act as this item submenu', max_length=50, null=True)),
                ('menu', modelcluster.fields.ParentalKey(help_text='Menu to which this item belongs', on_delete=django.db.models.deletion.CASCADE, related_name='navigation_menu_items', to='base_navigation.basenavigationsnippet')),
                ('menu_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.page', verbose_name='Page')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
