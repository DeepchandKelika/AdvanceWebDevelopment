from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from config import MONGO_URI
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


client = MongoClient(MONGO_URI)
db = client['recipe_db']
collection = db['recipes']


API_ID = '5ad2224f'
API_KEY = '38d2a6e6ed8512ffb2c8a803cccdc75b'


@app.route('/whatcanimake')
def what_can_i_make():
    render_template('whatcanimake.js')


@app.route('/', methods=['GET'])
def get_recipes():

    search_query = request.args.get('query')
    diet = request.args.get('diet')
    health = request.args.get('health')
    cuisineType = request.args.get('cuisineType')
    mealType = request.args.get('mealType')
    dishType = request.args.get('dishType')

    existing_recipe = collection.find_one({
        'search_query': search_query,
        'diet': diet,
        'health': health,
        'cuisineType': cuisineType,
        'mealType': mealType,
        'dishType': dishType
    })

    if existing_recipe:
        return jsonify(existing_recipe['recipe_data'])



    search_query = request.args.get('query')
    diet = request.args.get('diet')
    health = request.args.get('health')
    cuisineType = request.args.get('cuisineType')
    mealType = request.args.get('mealType')
    dishType = request.args.get('dishType')
    



    params = {
        'type': 'public',
        'q': search_query,
        'app_id': API_ID,
        'app_key': API_KEY,
        'diet': diet,
        'health':health,
        'cuisineType':cuisineType,
        'mealType': mealType,
        'dishType': dishType
    }
    

    response = requests.get('https://api.edamam.com/api/recipes/v2', params=params)

    if response.status_code == 200:
        recipe_data = response.json()
        collection.insert_one({
            'search_query': search_query,
            'diet': diet,
            'health': health,
            'cuisineType': cuisineType,
            'mealType': mealType,
            'dishType': dishType,
            'recipe_data': recipe_data
        })
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Request failed'})


@app.route('/recipe/<recipe_id>')
def specific_recipe_info(recipe_id):

    params = {
        'type': 'public',
        'random' : 'true',
        'app_id': API_ID,
        'app_key': API_KEY
    }



    response = requests.get('https://api.edamam.com//api/recipes/v2/{recipe_id}', params=params)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Request failed'})


if __name__ == '__main__':
    app.run(debug=True)
