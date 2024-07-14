

def get_statistics(response):
    msg = [f'{stat["base_stat"]} de {stat["stat"]["name"]}' for stat in response['stats']]
    return ', '.join(msg)
