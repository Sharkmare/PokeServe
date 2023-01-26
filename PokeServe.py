from flask import Flask, jsonify
import requests
import requests_cache

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

if __name__ == '__main__':
    app.run(debug=True)
