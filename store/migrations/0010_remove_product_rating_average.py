# Generated by Django 4.2.4 on 2023-09-27 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_comment_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='rating_average',
        ),
    ]
