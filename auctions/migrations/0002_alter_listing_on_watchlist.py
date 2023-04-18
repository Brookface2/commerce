# Generated by Django 4.1.7 on 2023-04-16 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='on_watchlist',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, related_name='watching_item', to='auctions.watchlist'),
        ),
    ]
