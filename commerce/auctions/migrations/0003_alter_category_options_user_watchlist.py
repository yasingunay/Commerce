# Generated by Django 4.2.5 on 2023-09-15 16:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0002_category_alter_user_id_listing"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "Categories"},
        ),
        migrations.AddField(
            model_name="user",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True, related_name="watchlist", to="auctions.listing"
            ),
        ),
    ]
