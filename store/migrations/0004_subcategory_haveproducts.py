# Generated by Django 3.0.8 on 2020-08-16 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20200727_0140'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='haveproducts',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
