# Generated by Django 4.2.4 on 2023-11-01 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='customization',
            field=models.TextField(default=' Not Available'),
        ),
    ]
