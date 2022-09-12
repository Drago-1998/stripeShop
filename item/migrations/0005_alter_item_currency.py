# Generated by Django 4.1.1 on 2022-09-11 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_itemtotax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='currency',
            field=models.CharField(choices=[('usd', 'US dollars'), ('rub', 'Russian rubles')], default='usd', max_length=3, verbose_name='Currency'),
        ),
    ]