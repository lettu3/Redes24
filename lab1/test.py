import requests

def print_linea(descripcion):
    """Imprime una línea con el número de test y su descripción """
    print(f"---- Test: {descripcion} ----\n")


# Obtener todas las películas
print_linea("obtener todas las películas")
response = requests.get('http://localhost:5000/peliculas')
peliculas = response.json()
print("Películas existentes:")
for pelicula in peliculas:
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
print()

# Agregar una nueva película
print_linea("Agregar una nueva película")
nueva_pelicula = {
    'titulo': 'Pelicula de prueba',
    'genero': 'Acción'
}
response = requests.post('http://localhost:5000/peliculas', json=nueva_pelicula)
if response.status_code == 201:
    pelicula_agregada = response.json()
    print("Película agregada:")
    print(f"ID: {pelicula_agregada['id']}, Título: {pelicula_agregada['titulo']}, Género: {pelicula_agregada['genero']}")
else:
    print("Error al agregar la película.")
print()

# Obtener detalles de una película específica
print_linea("obtener detalles de una película específica")
id_pelicula = 1  # ID de la película a obtener
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print("Error al obtener los detalles de la película.")
print()


# Actualizar los detalles de una película
print_linea("actualizar los detalles de una película")
id_pelicula = 1  # ID de la película a actualizar
datos_actualizados = {
    'titulo': 'Nuevo título',
    'genero': 'Comedia'
}
response = requests.put(f'http://localhost:5000/peliculas/{id_pelicula}', json=datos_actualizados)
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada:")
    print(f"ID: {pelicula_actualizada['id']}, Título: {pelicula_actualizada['titulo']}, Género: {pelicula_actualizada['genero']}")
else:
    print("Error al actualizar la película.")
print()


# Eliminar una película
print_linea("eliminar una película")
id_pelicula = 1  # ID de la película a eliminar
response = requests.delete(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    print("Película eliminada correctamente.")
else:
    print("Error al eliminar la película.")
print()

# Recomendar película random de cierto genero
print_linea("recomendar película random de cierto genero")
response = requests.get('http://localhost:5000/peliculas/recomendarPorGenero/Drama')
if response.status_code == 200:
    pelicula_recomendada = response.json()
    print("Detalles de la película recomendada:")
    print(f"ID: {pelicula_recomendada['id']}, Título: {pelicula_recomendada['titulo']},")
else:
    print("Error al obtener recomendación.")
print()

 
# Recomendar película para el próximo feriado
print_linea("recomendar película para el próximo feriado")
genero_pelicula = "Drama"
response = requests.get(f'http://localhost:5000/peliculas/recomendarFeriado/{genero_pelicula}')
if response.status_code == 200:
    pelicula_recomendada = response.json()
    print("Detalles de la película:")
    print(f"ID: {pelicula_recomendada['id']}, "
           + f"Título: {pelicula_recomendada['titulo']}, "
           + f"Género: {pelicula_recomendada['genero']}, \n"
           + f"Feriado: {pelicula_recomendada['feriado']}")
else:
    print("Error al obtener recomendación.")
