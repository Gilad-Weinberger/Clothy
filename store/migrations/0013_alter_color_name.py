# Generated by Django 4.2.4 on 2023-09-27 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_color_hex_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='name',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]
