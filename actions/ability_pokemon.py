

def get_ability(response):

    types_pokemon = []

    for abilities in response['abilities']:
        types_pokemon.append(abilities['ability']['name'])

    return ', '.join(types_pokemon)
