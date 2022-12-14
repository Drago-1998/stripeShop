# Generated by Django 4.1.1 on 2022-09-10 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('other', '0001_initial'),
        ('item', '0003_item_price_id_item_stripe_id_alter_item_currency'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemToTax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taxes_bundles', to='item.item', verbose_name='Item (Product)')),
                ('tax', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items_bundles', to='other.tax', verbose_name='Tax')),
            ],
        ),
    ]
