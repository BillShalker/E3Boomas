# Generated by Django 5.0.3 on 2024-03-09 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='picture',
            field=models.ImageField(upload_to='images/product_images/'),
        ),
    ]
