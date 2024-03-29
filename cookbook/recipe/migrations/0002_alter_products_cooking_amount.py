# Generated by Django 5.0.1 on 2024-01-26 15:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipe", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="cooking_amount",
            field=models.PositiveSmallIntegerField(
                default=0,
                help_text="Количество приготовлений",
                verbose_name="Количество приготовлений",
            ),
        ),
    ]
