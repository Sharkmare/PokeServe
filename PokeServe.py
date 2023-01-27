from flask import Flask, jsonify
import requests
import requests_cache
from math import floor

app = Flask(__name__)

# configure the cache to expire after 6 months (182.5 days)
requests_cache.install_cache('pokeapi_cache', expire_after=15778800)

@app.route('/pokemon/<string:name>', methods=['GET'])
def get_pokemon(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    response = requests.get(url)
    return jsonify(response.json())

#BASE STAT START
@app.route('/pokemon/<string:name>/stats/hp', methods=['GET'])
def get_pokemon_hp(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    response = requests.get(url)
    data = response.json()
    return jsonify(data["stats"][0]["base_stat"])

@app.route('/pokemon/<string:name>/stats/attack', methods=['GET'])
def get_pokemon_attack(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    response = requests.get(url)
    data = response.json()
    return jsonify(data["stats"][1]["base_stat"])

@app.route('/pokemon/<string:name>/stats/defense', methods=['GET'])
def get_pokemon_defense(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    response = requests.get(url)
    data = response.json()
    return jsonify(data["stats"][2]["base_stat"])

@app.route('/pokemon/<string:name>/stats/special-attack', methods=['GET'])
def get_pokemon_special_attack(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    response = requests.get(url)
    data = response.json()
    return jsonify(data["stats"][3]["base_stat"])

@app.route('/pokemon/<string:name>/stats/speed', methods=['GET'])
def get_pokemon_speed(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    response = requests.get(url)
    data = response.json()
    return jsonify(data["stats"][4]["base_stat"])

@app.route('/pokemon/<string:name>/stats/special-defense', methods=['GET'])
def get_pokemon_special_defense(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    response = requests.get(url)
    data = response.json()
    return jsonify(data["stats"][5]["base_stat"])

#BASE STAT END

#TYOING DATA
@app.route("/types/<name>", methods=["GET"])
def get_types(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)
    data = response.json()
    types = [t["type"]["name"] for t in data["types"]]
    return jsonify(types)
#TYPING DATA END

#COMPOUND STAT FUNCTION ADDITION START
@app.route('/pokemon/<string:name>/stats/all', methods=['GET'])
def get_pokemon_all_stats(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    response = requests.get(url)
    data = response.json()
    stats = {}
    for i in range(len(data["stats"])):
        stat_name = data["stats"][i]["stat"]["name"]
        stat_value = data["stats"][i]["base_stat"]
        stats[stat_name] = stat_value
    return jsonify(stats)
#COMPOUND STAT FUNCTION END

#SPRITE CODE START
def get_pokemon_data(name, shiny=False, back=False):
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    response = requests.get(url)
    data = response.json()
    if back:
        if shiny:
            return data["sprites"]["back_shiny"]
        else:
            return data["sprites"]["back_default"]
    else:
        if shiny:
            return data["sprites"]["front_shiny"]
        else:
            return data["sprites"]["front_default"]

@app.route('/pokemon/<string:name>/sprite', methods=['GET'])
def get_pokemon_sprite(name):
    return jsonify(get_pokemon_data(name, shiny=False, back=False))

@app.route('/pokemon/<string:name>/sprite/shiny', methods=['GET'])
def get_pokemon_shiny(name):
    return jsonify(get_pokemon_data(name, shiny=True, back=False))

@app.route('/pokemon/<string:name>/sprite/back', methods=['GET'])
def get_pokemon_back(name):
    return jsonify(get_pokemon_data(name, shiny=False, back=True))

@app.route('/pokemon/<string:name>/sprite/shiny/back', methods=['GET'])
def get_pokemon_shiny_back(name):
    return jsonify(get_pokemon_data(name, shiny=True, back=True))
#SPRITE CODE END

#MOVE CODE START
@app.route('/move/<string:move_name>', methods=['GET'])
def get_move_info(move_name):
    url = f'https://pokeapi.co/api/v2/move/{move_name}'
    response = requests.get(url)
    data = response.json()
    move = {}
    move["name"] = data["name"]
    move["power"] = data["power"]
    move["type"] = data["type"]["name"]
    move["accuracy"] = data["accuracy"]
    move["pp"] = data["pp"]
    return jsonify(move)

def check_valid_move(pokemon_name, move_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
    response = requests.get(url)
    data = response.json()
    moves = data["moves"]
    for move in moves:
        if move_name.lower() == move["move"]["name"].lower():
            learn_method = move["version_group_details"][0]["move_learn_method"]["name"]
            if learn_method == "level-up":
                learn_level = move["version_group_details"][0]["level_learned_at"]
                return jsonify({"valid": True, "learn_method":learn_method, "learn_level": learn_level})
            else:
                return jsonify({"valid": True, "learn_method":learn_method})
    return jsonify({"valid": False})
#MOVE CODE END

#POKEDEX START
@app.route('/pokedex-entry/<string:pokemon_name>/<string:version>/<string:language>', methods=['GET'])
def get_pokedex_entry(pokemon_name, version, language):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
    response = requests.get(url)
    data = response.json()
    species_url = data["species"]["url"]
    response = requests.get(species_url)
    species_data = response.json()
    for entry in species_data["flavor_text_entries"]:
        if entry["language"]["name"] == language and entry["version"]["name"] == version:
            return jsonify({"pokedex_entry": entry["flavor_text"]})
    return jsonify({"error": "Pokedex entry not found"})
#POKEDEX END

#MISC DATA START
@app.route('/pokemon/<string:pokemon_name>/versions', methods=['GET'])
def get_pokemon_versions(pokemon_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
    response = requests.get(url)
    data = response.json()
    versions = []
    for version in data['game_indices']:
        versions.append(version['version']['name'])
    return jsonify({"versions": versions})

@app.route('/versions/<string:version_name>/languages', methods=['GET'])
def get_version_languages(version_name):
    url = f'https://pokeapi.co/api/v2/version/{version_name}'
    response = requests.get(url)
    data = response.json()
    languages = []
    for language in data['names']:
        languages.append(language['language']['name'])
    return jsonify({"languages": languages})
#MISC DATA END

#ATTEMPTED DAMAGE CALC
@app.route('/damage/<string:attacker_name>/<string:move_name>/<string:defender_name>/<int:hp_ev>/<int:attack_ev>/<int:defense_ev>/<int:special_attack_ev>/<int:special_defense_ev>/<int:speed_ev>/<int:hp_iv>/<int:attack_iv>/<int:defense_iv>/<int:special_attack_iv>/<int:special_defense_iv>/<int:speed_iv>', methods=['GET'])
def calculate_damage(attacker_name, move_name, defender_name, hp_ev, attack_ev, defense_ev, special_attack_ev, special_defense_ev, speed_ev, hp_iv, attack_iv, defense_iv, special_attack_iv, special_defense_iv, speed_iv):
    # Get typing data
    types_url = 'https://pokeapi.co/api/v2/type'
    response = requests.get(types_url) 
    types_data = response.json()
    types = {}
    for type_data in types_data['results']:
        type_url = type_data['url']
        response = requests.get(type_url)
        type_info = response.json()
        types[type_info['name'].lower()] = type_info


    # Get attacker's data
    url = f'https://pokeapi.co/api/v2/pokemon/{attacker_name}'
    response = requests.get(url)
    attacker_data = response.json()

    # Get attacker's move data
    move_url = None
    for move in attacker_data['moves']:
        if move['move']['name'] == move_name:
            move_url = move['move']['url']
            break
    if not move_url:
        return jsonify({"error": f"{move_name} is not a valid move for {attacker_name}"})
    move_response = requests.get(move_url)
    move_data = move_response.json()

    # Get defender's data
    url = f'https://pokeapi.co/api/v2/pokemon/{defender_name}'
    response = requests.get(url)
    defender_data = response.json()

    # Get attacker's level, EVs, IVs, and moves
    level = 100 # Assume level 100 for attacker
    evs = {'hp': hp_ev, 'attack': attack_ev, 'defense': defense_ev, 'special-attack': special_attack_ev, 'special-defense': special_defense_ev, 'speed': speed_ev}
    ivs = {'hp': hp_iv, 'attack': attack_iv, 'defense': defense_iv, 'special-attack': special_attack_iv, 'special-defense': special_defense_iv, 'speed': speed_iv}
    # Calculate base stats
    base_stats = {stat['stat']['name']: stat['base_stat'] for stat in attacker_data['stats']}
    hp = floor((2 * base_stats['hp'] + ivs['hp'] + floor(evs['hp']/4)) * level / 100) + level + 10
    attack = floor(((2 * base_stats['attack'] + ivs['attack'] + floor(evs['attack']/4)) * level / 100) + 5)
    defense = floor(((2 * base_stats['defense'] + ivs['defense'] + floor(evs['defense']/4)) * level / 100) + 5)
    special_attack = floor(((2 * base_stats['special-attack'] + ivs['special-attack'] + floor(evs['special-attack']/4)) * level / 100) + 5)
    special_defense = floor(((2 * base_stats['special-defense'] + ivs['special-defense'] + floor(evs['special-defense']/4)) * level / 100) + 5)
    speed = floor(((2 * base_stats['speed'] + ivs['speed'] + floor(evs['speed']/4)) * level / 100) + 5)
    
    # Get defender's stats
    defender_stats = {stat['stat']['name']: stat['base_stat'] for stat in defender_data['stats']}

    # Get move's type, power, and category
    move_type = move_data['type']['name']
    move_power = move_data['power']
    move_category = move_data['damage_class']['name']

    # Get defender's types
    defender_types = [t['type']['name'] for t in defender_data['types']]

    # Calculate damage
    if move_category == 'physical':
        attack_stat = attack
        defense_stat = defense
    elif move_category == 'special':
        attack_stat = special_attack
        defense_stat = special_defense
    else:
        return jsonify({"error": "Invalid"})

    # Get type effectiveness
    effectiveness = 1
    for t in defender_types:
        for relation in types[move_type]['damage_relations']:
            if relation == t:
                effectiveness *= types[move_type]['damage_relations'][relation]['double_damage_from'] or 1
                effectiveness *= 2 if types[move_type]['damage_relations'][relation]['half_damage_from'] else 1
                effectiveness *= 0.5 if types[move_type]['damage_relations'][relation]['no_damage_from'] else 1

    # Calculate damage
    damage = floor((((2 * level) / 5 + 2) * move_power * attack_stat / defense_stat) / 50) + 2
    damage *= effectiveness

    # Return damage
    return jsonify({"damage": damage})
    #DAMAGE CALC END

#LEVEL CALC
@app.route("/pokemon/level/exp", methods=["GET"])
@app.route("/level/<string:name>/<int:exp>", methods=["GET"])
def calculate_level(name, exp):
    poke_data = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{name}").json()
    level = 0
    for level_data in poke_data["growth_rate"]["levels"]:
        if exp < level_data["experience"]:
            break
        level = level_data["level"]
    return jsonify({"level": level})

@app.route('/exp/<name>/<int:level>', methods=['GET'])
def exp_required(name, level):
    poke_data = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{name}').json()
    exp_groups = poke_data['growth_rate']['url']
    exp_data = requests.get(exp_groups).json()
    exp_to_reach_next_level = exp_data['experience'][level]
    return jsonify({'EXP required to reach level '+ str(level) : exp_to_reach_next_level})
#LEVEL CALC END

#EVO DATA
@app.route("/level/evolve/<name>")
def evolve(name):
    # Get the pokemon data from the pokeapi
    pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{name}").json()
    # Get the evolution chain data
    evolution_chain = requests.get(pokemon["species"]["url"]).json()["evolution_chain"]["url"]
    evolution_data = requests.get(evolution_chain).json()
    if evolution_data is not None:
        # Iterate through the evolution data to find the evolution that matches the current pokemon
        for evolution in evolution_data["chain"]["evolves_to"]:
            if evolution["species"]["name"] == name:
                level = evolution["evolution_details"][0]["min_level"] if "min_level" in evolution["evolution_details"][0] else None
                item = evolution["evolution_details"][0]["item"] if "item" in evolution["evolution_details"][0] else None
                return f"{name} can evolve at level {level} with the item {item}."
        return f"{name} does not have any evolutions."
    else:
        return f"{name} does not have any evolutions."
#EVO DATA END
    
if __name__ == '__main__':
    app.run(debug=True)
