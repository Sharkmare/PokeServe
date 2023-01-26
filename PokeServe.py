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

if __name__ == '__main__':
    app.run(debug=True)
