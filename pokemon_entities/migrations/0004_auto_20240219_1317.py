# Generated by Django 3.1.14 on 2024-02-19 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0003_auto_20240219_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonentity',
            name='stamina',
            field=models.IntegerField(null=True),
        ),
    ]