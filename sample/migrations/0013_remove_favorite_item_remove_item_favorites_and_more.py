# Generated by Django 4.1 on 2024-05-21 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0012_item_favorites_alter_item_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorite',
            name='item',
        ),
        migrations.RemoveField(
            model_name='item',
            name='favorites',
        ),
        migrations.AddField(
            model_name='favorite',
            name='items',
            field=models.ManyToManyField(blank=True, to='sample.item'),
        ),
    ]
