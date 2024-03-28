# Implementacion realizada por Nahuel Fernandez, Ignacio Gomez Barrios y Luciano Rojo

import random
from unidecode import unidecode
from flask import Flask, jsonify, request
import proximo_feriado as feriado

app = Flask(__name__)
peliculas = [
    {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
    {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'},
    {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
    {'id': 4, 'titulo': 'Jurassic Park', 'genero': 'Aventura'},
    {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
    {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
    {'id': 7, 'titulo': 'The Lord of the Rings', 'genero': 'Fantasía'},
    {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
    {'id': 9, 'titulo': 'Inception', 'genero': 'Ciencia ficción'},
    {'id': 10, 'titulo': 'The Shawshank Redemption', 'genero': 'Drama'},
    {'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'Crimen'},
    {'id': 12, 'titulo': 'Fight Club', 'genero': 'Drama'}
]

def obtener_peliculas():
    """Obtiene un json de todas las películas"""
    return jsonify(peliculas)

def obtener_pelicula(id):
    """Retorna un json de la pelicula con el id dado"""
    #Itero sobre la lista de películas hasta encontrar la que tiene el id que busco.
    pelicula_encontrada = next((pelicula for pelicula in peliculas if pelicula['id'] == id), None)
    if pelicula_encontrada:
        return jsonify(pelicula_encontrada)
    else:
        return jsonify({'mensaje': 'Película no encontrada'}), 404


def agregar_pelicula():
    """Añade una película a la lista de películas."""
    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(nueva_pelicula)
    print(peliculas)
    return jsonify(nueva_pelicula), 201


def actualizar_pelicula(id):
    """Actualiza los datos de la película"""
    pelicula_a_actualizar = next((p for p in peliculas if p['id'] == id), None)
    if pelicula_a_actualizar is None:
        return jsonify({'mensaje': f'Película con id {id} no encontrada'}), 404
    
    #nuestro request, en formato json
    request_data = request.json 
    if 'titulo' in request_data:
        pelicula_a_actualizar['titulo'] = request_data['titulo']
    if 'genero' in request_data:
        pelicula_a_actualizar['genero'] = request_data['genero']

    return jsonify(pelicula_a_actualizar), 200



def eliminar_pelicula(id):
    """Busca una película por su ID y la elímina de la lista"""
    pelicula_a_eliminar = next((pelicula for pelicula in peliculas if pelicula['id'] == id), None)
    if pelicula_a_eliminar:
        peliculas.remove(pelicula_a_eliminar)
        return jsonify({'mensaje': 'Película eliminada correctamente'}), 200
    else:
        return jsonify({'mensaje': 'Película no encontrada'}), 404

def obtener_por_genero(genero):
    """Busca películas por genero y las devuelve en un json."""
    peliculas_genero =  [pelicula for pelicula in peliculas if unicode_to_url(pelicula['genero']) == unicode_to_url(genero)]
    if peliculas_genero:
        return jsonify(peliculas_genero)
    else:
        return jsonify(
            {'mensaje': 'El genero provisto no existe o no hay películas que se correspondan'}), 404


def obtener_nuevo_id():
    """Retorna un nuevo id"""
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1

def buscar_por_string(palabra):
    """Retorna una película con título <palabra>"""
    #lower() convierte todo el string en minúscula para no tener problemas.
    peliculas_nombre = [pelicula for pelicula in peliculas
                        if unicode_to_url(palabra) in unicode_to_url(pelicula['titulo'])]
    if peliculas_nombre:
        return jsonify(peliculas_nombre)
    else:
        return jsonify({'mensaje': 'No se encontraron coincidencias'}), 404

def recomendar_random():
    """Devuelve una película random de la lista"""
    return jsonify(random.choice(peliculas))

def recomendar_random_gen(genero):
    "Devuelve una película random con genero <genero>"
    peliculas_genero =  [pelicula for pelicula in peliculas if unicode_to_url(pelicula['genero']) == unicode_to_url(genero)]
    if peliculas_genero:
        pelicula_recomendada = random.choice(peliculas_genero)
        return jsonify(pelicula_recomendada), 200
    else:
        return jsonify({'mensaje': 'No se encontraron coincidencias'}), 404

def recomendar_feriado_gen(genero):
    """Devuelve un json con la película del genero dado"""
    next_holiday = feriado.NextHoliday()
    next_holiday.fetch_holidays()
    response = recomendar_random_gen(genero)
    if response[1] == 200:
        pelicula_json = response[0].get_json()
        pelicula_json['feriado'] = next_holiday.holiday
        return jsonify(pelicula_json)
    else:
        return jsonify({'mensaje': 'No se encontraron coincidencias'}), 404


def unicode_to_url(string):
    """Transforma un string unicode a un formato manejable en urls """
    #unidecode("HÓLÁ QÚÉ TÁL") = "HOLA QUE TAL"
    string = unidecode(string)

    #string.lower("HOLA QUE TAL") = "hola que tal"
    string = string.lower()

    #string.replace(" ", "-") = "hola-que-tal"
    string = string.replace(" ", "-")
    return string

app.add_url_rule('/peliculas', 'obtener_peliculas', obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula', obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula', agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', eliminar_pelicula, methods=['DELETE'])
app.add_url_rule('/peliculas/obtenerPorGenero/<string:genero>',
                  'obtener_por_genero', obtener_por_genero, methods=['GET'])
app.add_url_rule('/peliculas/buscarPorString/<string:palabra>',
                  'buscar_por_string', buscar_por_string, methods=['GET'])
app.add_url_rule('/peliculas/recomendar', 'recomendar_random',
                  recomendar_random, methods=['GET'])
app.add_url_rule('/peliculas/recomendarPorGenero/<string:genero>',
                  'recomendar_random_gen', recomendar_random_gen, methods=['GET'])
app.add_url_rule('/peliculas/recomendarFeriado/<string:genero>',
                  'recomendar_feriado_gen', recomendar_feriado_gen, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
