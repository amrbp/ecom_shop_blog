# Generated by Django 3.1.6 on 2021-03-26 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210326_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]