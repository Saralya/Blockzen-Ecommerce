# Generated by Django 3.0.8 on 2020-08-27 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_order_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryMan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('contactnumber', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='OrderDelivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignDate', models.DateTimeField(auto_now_add=True)),
                ('deliveryman', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.DeliveryMan')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.Order')),
            ],
        ),
    ]
