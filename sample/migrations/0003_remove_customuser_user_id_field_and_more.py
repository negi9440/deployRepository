# Generated by Django 4.1 on 2024-04-26 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0002_remove_favorite_item_favorite_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='user_id_field',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='メールアドレス'),
        ),
    ]
