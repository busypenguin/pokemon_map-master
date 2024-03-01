import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import (Pokemon, PokemonEntity)
from django.utils import timezone


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):

    pokemons = Pokemon.objects.all()
    pokemons_entity = PokemonEntity.objects.filter(appeared_at__lt=timezone.localtime(), disappeared_at__gt=timezone.localtime())
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon in pokemons:
        if pokemon.photo:
            photo = str(pokemon.photo.url)
        else:
            photo = None

        for pokemon_entity in pokemons_entity:
            add_pokemon(
                folium_map, pokemon_entity.latitude,
                pokemon_entity.longitude,
                request.build_absolute_uri(photo)
                )

    pokemons_on_page = []
    for pokemon in pokemons:
        if pokemon.photo:
            photo = str(pokemon.photo.url)
        else:
            photo = None
        
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(photo),
            'title_ru': pokemon,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    # with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
    #     json_pokemons = json.load(database)['pokemons']
        
    # for json_pokemon in json_pokemons:
    #     if pokemon:
    #         dict_pokemon['img_url'] = json_pokemons[pokemon]['img_url']
    #         dict_pokemon['title_ru'] = json_pokemons[pokemon]['title_ru']
    pokemon = Pokemon.objects.get(id=pokemon_id)
    dict_pokemon = {}
    if pokemon.photo:
        photo = str(pokemon.photo.url)
    else:
        photo = None
        
    if pokemon.id == int(pokemon_id):
        requested_pokemon = PokemonEntity.objects.filter(pokemon=pokemon, appeared_at__lt=timezone.localtime(), disappeared_at__gt=timezone.localtime())

    dict_pokemon['img_url'] = request.build_absolute_uri(photo)
    dict_pokemon['title_ru'] = pokemon.title
    dict_pokemon['description'] = pokemon.description
        # return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon:
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(photo)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': dict_pokemon
    })
