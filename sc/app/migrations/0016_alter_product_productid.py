# Generated by Django 5.0.4 on 2024-04-20 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_rename_title_product_food_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ProductId',
            field=models.CharField(max_length=20),
        ),
    ]
