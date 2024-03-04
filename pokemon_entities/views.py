import folium
import json

from django.shortcuts import get_object_or_404
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


def check_pokemon_photo(pokemon):
    if pokemon.photo:
        return str(pokemon.photo.url)
    else:
        return DEFAULT_IMAGE_URL


def find_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    return pokemon


def show_all_pokemons(request):

    pokemons = Pokemon.objects.all()
    right_now = timezone.localtime()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=right_now, disappeared_at__gt=right_now)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon in pokemons:
        for pokemon_entity in pokemon_entities:
            add_pokemon(
                folium_map, pokemon_entity.latitude,
                pokemon_entity.longitude,
                request.build_absolute_uri(check_pokemon_photo(pokemon))
                )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(check_pokemon_photo(pokemon)),
            'title_ru': pokemon,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = find_pokemon(request, pokemon_id)
    dict_pokemon = {}
    previous_evolution_pokemon = {}
    next_evolution_pokemon = {}
    if pokemon.id == int(pokemon_id):
        requested_pokemon = PokemonEntity.objects.filter(pokemon=pokemon, appeared_at__lt=timezone.localtime(), disappeared_at__gt=timezone.localtime())

    dict_pokemon = {
        'img_url': request.build_absolute_uri(check_pokemon_photo(pokemon)),
        'title_ru': pokemon.title,
        'description': pokemon.description,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
    }

    if pokemon.previous_evolution:
        new_pokemon = pokemon.previous_evolution
        previous_evolution_pokemon = {
            'title_ru': new_pokemon.title,
            'pokemon_id': new_pokemon.id,
            'img_url': request.build_absolute_uri(check_pokemon_photo(new_pokemon)),
            'previous_evolution': previous_evolution_pokemon
        }
    if pokemon.next_evolutions.all():
        new_pokemon1 = pokemon.next_evolutions.get()
        next_evolution_pokemon = {
            'title_ru': new_pokemon1.title,
            'pokemon_id': new_pokemon1.id,
            'img_url': request.build_absolute_uri(check_pokemon_photo(new_pokemon1)),
            'next_evolution': next_evolution_pokemon
        }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon:
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(check_pokemon_photo(pokemon))
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': dict_pokemon
    })
