# Generated by Django 4.2.4 on 2023-09-27 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_product_rating_average_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]
