

def get_moves(response):

    types_pokemon = []

    for i in range(5):
        types_pokemon.append(response['moves'][i]['move']['name'])

    return ', '.join(types_pokemon)

