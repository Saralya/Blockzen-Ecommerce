# Generated by Django 3.0.8 on 2020-08-26 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20200825_1702'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('statusfor', models.CharField(blank=True, max_length=200, null=True)),
                ('isActive', models.BooleanField(blank=True, default=True, null=True)),
            ],
        ),
    ]