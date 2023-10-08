# Generated by Django 4.2.4 on 2023-09-27 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_color_remove_product_colors_product_colors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discount_amount',
        ),
        migrations.RemoveField(
            model_name='product',
            name='discount_percentage',
        ),
        migrations.AddField(
            model_name='product',
            name='discount_type',
            field=models.CharField(choices=[('percentage', 'Percentage'), ('amount', 'Amount'), ('none', 'None')], default='none', max_length=10),
        ),
        migrations.AddField(
            model_name='product',
            name='discount_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
