# Generated by Django 4.1.7 on 2023-04-16 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_listing_on_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
