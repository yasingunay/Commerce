# Generated by Django 4.2.5 on 2023-09-15 18:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0003_alter_category_options_user_watchlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="bids",
            field=models.ManyToManyField(
                blank=True, related_name="bidder", to="auctions.listing"
            ),
        ),
    ]
