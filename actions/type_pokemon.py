

def get_types(response):

    types_pokemon = []

    for types in response['types']:
        types_pokemon.append(types['type']['name'])

    return ', '.join(types_pokemon)
