# Generated by Django 3.1.14 on 2024-03-04 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0017_auto_20240302_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonentity',
            name='pokemon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon', to='pokemon_entities.pokemon', verbose_name='Покемон'),
        ),
    ]
