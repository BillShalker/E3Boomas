# Generated by Django 5.0.3 on 2024-03-10 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='picture',
            field=models.ImageField(upload_to='images/products/'),
        ),
    ]