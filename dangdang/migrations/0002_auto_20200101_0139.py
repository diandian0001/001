# Generated by Django 2.0.6 on 2019-12-31 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dangdang', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tshopcar',
            name='make_prices',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='tshopcarall',
            name='shop_status',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
