from typing import List, Union
from fastapi import FastAPI
import mysql.connector

# Conexión a la base de datos
mydb = mysql.connector.connect(
    host="db",
    port=3306,
    user="root",
    password="root",
    database="sakila"
)

# Crear un cursor
cursor = mydb.cursor(dictionary=True)

app = FastAPI()

# Endpoint 1: Obtener todos los actores
@app.get("/v1/inventory")
def get_inventory():
    """
    Obtiene datos de inventario de la base de datos, organizando películas por tienda.

    Esta función realiza los siguientes pasos:
    1. Recupera todos los registros de inventario, tiendas y películas de la base de datos.
    2. Para cada tienda, inicializa una lista 'movies' para almacenar la información de las películas.
    3. Recorre el inventario para encontrar películas disponibles en cada tienda.
    4. Para cada película en una tienda, comprueba si ya está listada en la lista 'movies' de la tienda:
        - Si está presente, incrementa el 'count' (contador) de esa película.
        - Si no está presente, añade la película a la lista con un 'count' de 1.
    5. El resultado es que la lista 'movies' de cada tienda contiene películas únicas con un contador de cuántas veces aparece cada película en el inventario de esa tienda.

    Nota:
        - Asume que el cursor de la base de datos y la conexión ya están establecidos y disponibles como 'cursor'.
        - Modifica la estructura de datos 'stores' in situ añadiendo una clave 'movies' a cada diccionario de tienda.
    """
    cursor.execute("SELECT * FROM inventory")
    inventorys = cursor.fetchall()
    cursor.execute("SELECT * FROM store")
    stores = cursor.fetchall()
    cursor.execute("SELECT * FROM film")
    films = cursor.fetchall()

    for store in stores:
        store["movies"] = []
        for i in inventorys:
            if i["store_id"] == store["store_id"]:
                for film in films:
                    if film["film_id"] == i["film_id"]:
                        # Verificar si la película ya está en la lista de películas de la tienda
                        movie_found = False
                        for movie in store["movies"]:
                            if movie["film_id"] == film["film_id"]:
                                movie["count"] += 1
                                movie_found = True
                                break
                        # Si no se encontró, agregar la película a la lista
                        if not movie_found:
                            store["movies"].append({"film_id": film["film_id"], "title": film["title"], "count": 1})


    return {"stores": stores}

# Endpoint 2: Obtener todas las películas
@app.get("/v1/movies")
def get_all_movies():
    
    cursor.execute("SELECT * FROM film")
    movies = cursor.fetchall()
    
    cursor.execute("SELECT * FROM film_actor")
    film_actors = cursor.fetchall()

    cursor.execute("SELECT * FROM actor")
    actors = cursor.fetchall()

    for movie in movies:
        movie["actors"] = []
        for film_actor in film_actors:
            if film_actor["film_id"] == movie["film_id"]:
                for actor in actors:
                    if actor["actor_id"] == film_actor["actor_id"]:
                        movie["actors"].append(actor)

    return {"movies": movies}
            

# Endpoint 3: Obtener todos los clientes
@app.get("/v1/customers")
def get_all_customers():
    cursor.execute("SELECT * FROM customer")
    customers = cursor.fetchall()
    cursor.execute("SELECT * FROM rental")
    rentals = cursor.fetchall()
    cursor.execute("SELECT* FROM payment")
    payments = cursor.fetchall()

    for customer in customers:
        customer["rentals"] = []
        for rental in rentals:
            if rental["customer_id"] == customer["customer_id"]:
               
                rental["payments"] = []
                for payment in payments:
                    if payment["rental_id"] == rental["rental_id"]:
                        rental["payments"].append(payment)
                customer["rentals"].append(rental)
    return {"customers": customers}



# Endpoint 4: Obtener todos los actores optimizado
@app.get("/v2/actors")
def get_all_actors():


    cursor.execute("SELECT * FROM actor")
    actors = cursor.fetchall()

    
    return {"actors": actors}

# Endpoint 5: Obtener todas las películas optimizado
@app.get("/v2/movies")
def get_all_movies():
    
    cursor.execute("SELECT * FROM film ")
    movies = cursor.fetchall()

    return {"movies": movies}

# Endpoint 6: Obtener todos los clientes optimizado
@app.get("/v2/customers")
def get_all_customers():
    cursor.execute("SELECT * FROM customer")
    customers = cursor.fetchall()
    return {"customers": customers}