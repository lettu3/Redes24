from flask import Flask, jsonify, request

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

#Para probar una función: primero correr la app con python main.py (la hostea)
#                         Tendría que aparecer "Running on http://127.0.0.1:5000", hay que poner eso en la url de algún navegador.
#                         Manipulando el formato de esa url como detalla mas abajo el código vamos probando cada función ejecutando el método que le corresponda.


#Para buscar una película (por ID en este caso) --> pelicula_encontrada = next((pelicula for pelicula in peliculas if pelicula['id'] == id), None)



def obtener_peliculas():
    return jsonify(peliculas)

#Recibe un ID y devuelve la película asociada. 
def obtener_pelicula(id):
    #Itero sobre la lista de películas hasta encontrar la que tiene el id que busco.
    pelicula_encontrada = next((pelicula for pelicula in peliculas if pelicula['id'] == id), None)
    if pelicula_encontrada: #Cualquier cosa distinta de null se interpreta como true, null se interpreta como falso.
        return jsonify(pelicula_encontrada)
    else:
        return jsonify({'mensaje': 'Película no encontrada'}), 404


def agregar_pelicula():
    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(nueva_pelicula)
    print(peliculas)
    return jsonify(nueva_pelicula), 201


def actualizar_pelicula(id): #pendiente
    # Lógica para buscar la película por su ID y actualizar sus detalles
    pelicula_a_actualizar = next((pelicula for pelicula in peliculas if pelicula['id'] == id), None)

    return jsonify(pelicula_actualizada)


def eliminar_pelicula(id): #Falta probar, ver como usar el metodo DELETE
    # Lógica para buscar la película por su ID y eliminarla
    global peliculas #Global porque la lista de películas es ajena a la función y la voy a reemplazar usando el mismo nombre.
    pelicula_a_eliminar = next((pelicula for pelicula in peliculas if pelicula['id'] == id), None)
    if pelicula_a_eliminar:
        #Sobreescribo la lista de películas con una idéntica pero sin la pelicula que quiero eliminar, osea con las que tienen un ID != id.
        peliculas = [pelicula for pelicula in peliculas if pelicula['id'] != id]
        return jsonify({'mensaje': 'Película eliminada correctamente'}), 200
    else:
        return jsonify({'mensaje': 'Película no encontrada'}), 404
    
def obtener_por_genero(genero):
    peliculas_genero =  [pelicula for pelicula in peliculas if pelicula['genero'] == genero]
    if peliculas_genero:
        return jsonify(peliculas_genero)
    else: 
        return jsonify({'mensaje': 'El genero provisto no existe o no hay películas que se correspondan'}), 404
    

def obtener_nuevo_id():
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1


app.add_url_rule('/peliculas', 'obtener_peliculas', obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula', obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula', agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', eliminar_pelicula, methods=['DELETE'])
app.add_url_rule('/peliculas/<string:genero>', 'obtener_por_genero', obtener_por_genero, methods=['GET'])

if __name__ == '__main__':
    app.run()















































