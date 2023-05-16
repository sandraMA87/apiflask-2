"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



@app.route('/user', methods=['GET'])
def get_users():

    users = User.query.all()
    user_list = [element.serialize() for element in users]


    return jsonify(user_list), 200



# GET DE PLANET-GALAXY

@app.route('/planet-galaxy', methods=['GET'])
def get_relation_planet_galaxy():
    planets = Planet.query.all()
    response = []
    for planet in planets:
        response.append({
            'planet': planet.name,
            'galaxy_id': planet.galaxy_id,
            'galaxy_name': planet.galaxy.name
        })
    return jsonify(response)


# GET DE PLANETS

@app.route('/planet', methods=['GET'])
def get_planets():
    allPlanets = Planet.query.all()
    result = [element.serialize() for element in allPlanets]
    return jsonify(result), 200


# POST DE FAVORITE DE PLANET_ID
current_logged_user_id = 1

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    
    user = User.query.get(current_logged_user_id)

    new_favorite = Favorite(user_id=current_logged_user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        "msg": "Nuevo planeta agregado correctamente", 
        "favorite": new_favorite.serialize()
    }

    return jsonify(response_body), 200



# POST DE PLANETS

@app.route('/planet', methods=['POST'])
def post_planet():

    # obtener los datos de la petición que están en formato JSON a un tipo de datos entendibles por pyton (a un diccionario). En principio, en esta petición, deberían enviarnos 3 campos: el nombre, la descripción del planeta y la población
    data = request.get_json()

    # creamos un nuevo objeto de tipo Planet
    planet = Planet(name=data['name'], description=data['description'])

    # añadimos el planeta a la base de datos
    db.session.add(planet)
    db.session.commit()

    return jsonify(planet.serialize()), 200

# DELETE DE PLANETS

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite = Favorite.query.filter_by(user_id=current_logged_user_id, planet_id=planet_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        response_body = {
            "msg": "Planeta favorito eliminado correctamente"
        }
        return jsonify(response_body), 200
   



# GET DE CHARACTERS

@app.route('/character', methods=['GET'])
def get_character():
    allCharacters = Character.query.all()
    result = [element.serialize() for element in allCharacters]
    return jsonify(result), 200



# GET DE CHARACTER_ID
    
@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    
    user = User.query.get(current_logged_user_id)

    new_favorite = Favorite(user_id=current_logged_user_id, character_id=character_id)
    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        "msg": "Nuevo character agregado correctamente", 
        "favorite": new_favorite.serialize()
    }

    return jsonify(response_body), 200



# POST DE CHARACTERS

@app.route('/character', methods=['POST'])
def post_character():

    # obtener los datos de la petición que están en formato JSON a un tipo de datos entendibles por pyton (a un diccionario). En principio, en esta petición, deberían enviarnos 3 campos: el nombre, la descripción del planeta y la población
    data = request.get_json()

    # creamos un nuevo objeto de tipo Character
    character = Character(name=data['name'], gender=data['gender'])

    # añadimos el character a la base de datos
    db.session.add(character)
    db.session.commit()

    return jsonify(character.serialize()), 200

# DELETE DE CHARACTERS

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    favorite = Favorite.query.filter_by(user_id=current_logged_user_id, character_id=character_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        response_body = {
            "msg": "Personaje favorito eliminado correctamente"
        }
        return jsonify(response_body), 200


# GET DE FAVORITES DE USERS


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    
    user = User.query.get(current_logged_user_id)
    favorites = user.favorites
    serialized_favorites = [f.serialize() for f in favorites]

    response_body = {
        "msg": f"Aqui tienes los favoritos de {user.email}",
        "favorites": serialized_favorites
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)