# Generated by Django 3.1.5 on 2021-01-06 21:56

import blog.streamblocks
from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtailmetadata.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('wagtailcore', '0059_apply_collection_ordering'),
        ('blog', '0006_auto_20210106_2123'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlatPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('subtitle', models.CharField(blank=True, max_length=255, null=True, verbose_name='Subtitle')),
                ('body', wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.RichTextBlock(icon='fa-paragraph', label='Text')), ('section_heading', blog.streamblocks.SectionHeading()), ('blockquote', blog.streamblocks.Blockquote()), ('single_img', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock('Image')), ('url', wagtail.core.blocks.URLBlock(label='URL', required=False)), ('caption', wagtail.core.blocks.CharBlock(label='Caption', required=False))]))], blank=True, null=True)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('search_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Search image')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtailmetadata.models.WagtailImageMetadataMixin, 'wagtailcore.page', models.Model),
        ),
    ]
