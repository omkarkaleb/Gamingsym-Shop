# Generated by Django 3.2.4 on 2021-07-06 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='country',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
