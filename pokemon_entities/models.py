from django.db import models  # noqa F401


class Pokemon(models.Model):
    """Покемон"""
    title = models.CharField(max_length=200,
                             verbose_name='Имя')
    description = models.TextField(blank=True,
                                   verbose_name='Описание')
    photo = models.ImageField(blank=True,
                              verbose_name='Фото')
    title_en = models.CharField(max_length=200,
                                blank=True,
                                verbose_name='Имя на английском')
    title_jp = models.CharField(max_length=200,
                                blank=True,
                                verbose_name='Имя на японском')
    previous_evolution = models.ForeignKey('Pokemon',
                                           on_delete=models.CASCADE,
                                           null=True, blank=True,
                                           related_name='next_evolutions',
                                           verbose_name='Из кого эволюционировал')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    """Сущность покемона"""
    pokemon = models.ForeignKey(Pokemon,
                                on_delete=models.CASCADE,
                                related_name='pokemon',
                                verbose_name='Покемон')
    latitude = models.FloatField(null=True,
                                 blank=True,
                                 verbose_name='Широта')
    longitude = models.FloatField(null=True,
                                  blank=True,
                                  verbose_name='Долгота')
    appeared_at = models.DateTimeField(null=True,
                                       blank=True,
                                       verbose_name='Появился')
    disappeared_at = models.DateTimeField(null=True,
                                          blank=True,
                                          verbose_name='Исчез')
    level = models.IntegerField(null=True,
                                blank=True,
                                verbose_name='Уровень')
    health = models.IntegerField(null=True,
                                 blank=True,
                                 verbose_name='Здоровье')
    strenght = models.IntegerField(null=True,
                                   blank=True,
                                   verbose_name='Атака')
    defence = models.IntegerField(null=True,
                                  blank=True,
                                  verbose_name='Защита')
    stamina = models.IntegerField(null=True,
                                  blank=True,
                                  verbose_name='Выносливость')
