from django.db import models  # noqa F401

# your models here


class Pokemon(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(blank=True)

    def __str__(self):
        if self.title:
            return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)  #широта
    longitude = models.FloatField(null=True, blank=True)  #долгота
    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    health = models.IntegerField(null=True, blank=True)
    strenght = models.IntegerField(null=True, blank=True)
    defence = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)
