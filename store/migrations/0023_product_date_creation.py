# Generated by Django 3.0.8 on 2020-11-21 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_auto_20201121_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
