# Generated by Django 3.1.6 on 2021-03-30 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_product_digital'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='content',
            field=models.TextField(default='', editable=False, max_length=50),
        ),
    ]
