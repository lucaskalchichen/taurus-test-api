from typing import List, Union
from fastapi import FastAPI
import mysql.connector

import aiomysql



# Conexión a la base de datos
async def get_connection():
    return await aiomysql.connect(
        host="db",
        port=3306,
        user="root",
        password="root",
        db="sakila",
        autocommit=True
    )


app = FastAPI()

# Endpoint 1: Obtener el inventario de peliculas por tienda
@app.get("/v1/inventory")
async def get_inventory():
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
    conn = await get_connection()
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        # Obtener todos los registros de inventario, tiendas y películas
        await cursor.execute("SELECT * FROM inventory")
        inventorys = await cursor.fetchall()
        await cursor.execute("SELECT * FROM store")
        stores = await cursor.fetchall()
        await cursor.execute("SELECT * FROM film")
        films = await cursor.fetchall()
    conn.close()


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
async def get_all_movies():
    """
    Recupera todas las películas con sus actores correspondientes.

    Tablas consultadas:
    - film: Para obtener la información básica de todas las películas
    - film_actor: Para obtener las relaciones entre películas y actores
    - actor: Para obtener la información de los actores

    Proceso:
    1. Ejecuta tres consultas separadas para obtener películas, relaciones film-actor y actores.
    2. Para cada película, identifica sus actores recorriendo las tablas de relaciones.
    3. Agrega la información de los actores a cada película mediante procesamiento en memoria.

    Respuesta:
    Un objeto JSON con una clave "movies" que contiene un array de películas,
    donde cada película incluye un array "actors" con los actores que participan en ella.
    """

    conn = await get_connection()
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        # Obtener todos los registros de películas, actores y la relación entre ellos
        await cursor.execute("SELECT * FROM film")
        movies = await cursor.fetchall()
        await cursor.execute("SELECT * FROM film_actor")
        film_actors = await cursor.fetchall()
        await cursor.execute("SELECT * FROM actor")
        actors = await cursor.fetchall()
    conn.close()
    
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
async def get_all_customers():
    """
    Recupera todos los clientes con sus alquileres asociados.

    Tablas consultadas:
    - customer: Para obtener la información básica de todos los clientes
    - rental: Para obtener los alquileres realizados por cada cliente

    Proceso:
    1. Ejecuta dos consultas separadas para obtener clientes y alquileres.
    2. Para cada cliente, identifica sus alquileres mediante procesamiento en memoria.
    3. Agrega la lista de alquileres a cada cliente.

    Respuesta:
    Un objeto JSON con una clave "customers" que contiene un array de clientes,
    donde cada cliente incluye un array "rentals" con sus alquileres.
    """


    conn = await get_connection()
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        # Obtener todos los registros de clientes, alquileres y pagos
        await cursor.execute("SELECT * FROM customer")
        customers = await cursor.fetchall()
        await cursor.execute("SELECT * FROM rental")
        rentals = await cursor.fetchall()
    conn.close()

    for customer in customers:
        customer["rentals"] = []
        for rental in rentals:
            if rental["customer_id"] == customer["customer_id"]:
                customer["rentals"].append(rental)
    return {"customers": customers}



# Endpoint 4: Obtener inventario optimizado
@app.get("/v2/inventory")
async def get_inventory():
    """
    Versión optimizada del endpoint de inventario utilizando JOINs y agregaciones SQL.

    Tablas consultadas:
    - store, inventory y film: Unidas mediante JOINs en una sola consulta

    Proceso:
    1. Ejecuta una única consulta SQL con JOINs entre store, inventory y film.
    2. Utiliza GROUP BY y COUNT para calcular cuántas copias de cada película hay en cada tienda.
    3. Ordena los resultados por tienda y título de película.
    4. Procesa los resultados para estructurarlos jerárquicamente por tienda.

    Respuesta:
    Un objeto JSON con una clave "stores" que contiene un array de tiendas,
    donde cada tienda incluye un array "movies" con las películas disponibles
    y la cantidad de copias de cada una.
    """


    conn = await get_connection()
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute("""
                    SELECT s.store_id,f.film_id,f.title,
                    COUNT(i.inventory_id) AS cantidad
                    FROM
                    store s
                    JOIN inventory i ON s.store_id = i.store_id
                    JOIN film f ON i.film_id = f.film_id
                    GROUP BY s.store_id, f.film_id, f.title
                    ORDER BY s.store_id, f.title;
                   """)
        rows = await cursor.fetchall()
    conn.close()

    # Organizar la respuesta agrupando por tienda
    stores = {}
    for row in rows:
        store_id = row["store_id"]
        movie = {
            "film_id": row["film_id"],
            "title": row["title"],
            "count": row["cantidad"]
        }
        if store_id not in stores:
            stores[store_id] = {"store_id": store_id, "movies": []}
        stores[store_id]["movies"].append(movie)
    return {"stores": list(stores.values())}

# Endpoint 5: Obtener películas optimizado
@app.get("/v2/movies")
async def get_all_movies():
    """
    Versión optimizada del endpoint de películas utilizando JOINs SQL.

    Tablas consultadas:
    - film, film_actor y actor: Unidas mediante LEFT JOINs en una sola consulta

    Proceso:
    1. Ejecuta una única consulta SQL con LEFT JOINs para obtener películas con sus actores.
    2. Procesa los resultados para agrupar actores por película en una estructura jerárquica.
    3. Maneja adecuadamente películas sin actores gracias al uso de LEFT JOIN.

    Respuesta:
    Un objeto JSON con una clave "movies" que contiene un array de películas,
    donde cada película incluye un array "actors" con los actores que participan en ella.
    """

    conn = await get_connection()
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        query = """
        SELECT 
            f.film_id, f.title, f.description, f.release_year,
            a.actor_id, a.first_name, a.last_name
        FROM film f
        LEFT JOIN film_actor fa ON f.film_id = fa.film_id
        LEFT JOIN actor a ON fa.actor_id = a.actor_id
    """
        await cursor.execute(query)
        rows = await cursor.fetchall()
    conn.close()

    movies_dict = {}
    for row in rows:
        film_id = row["film_id"]
        if film_id not in movies_dict:
            movies_dict[film_id] = {
                "film_id": film_id,
                "title": row["title"],
                "description": row["description"],
                "release_year": row["release_year"],
                "actors": []
            }
        if row["actor_id"]:
            actor = {
                "actor_id": row["actor_id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"]
            }
            movies_dict[film_id]["actors"].append(actor)

    return {"movies": list(movies_dict.values())}

# Endpoint 6: Obtener clientes optimizado
@app.get("/v2/customers")
async def get_all_customers():
    """
    Versión optimizada del endpoint de clientes utilizando JOINs SQL multinivel.

    Tablas consultadas:
    - customer, rental y payment: Unidas mediante LEFT JOINs en una sola consulta

    Proceso:
    1. Ejecuta una única consulta SQL con LEFT JOINs para obtener clientes, 
       sus alquileres y los pagos asociados a cada alquiler.
    2. Procesa los resultados para crear una estructura jerárquica de tres niveles:
       clientes -> alquileres -> pagos.
    3. Maneja adecuadamente clientes sin alquileres y alquileres sin pagos.

    Respuesta:
    Un objeto JSON con una clave "customers" que contiene un array de clientes,
    donde cada cliente incluye sus alquileres y cada alquiler incluye sus pagos asociados.
    """

    conn = await get_connection()
    async with conn.cursor(aiomysql.DictCursor) as cursor:

        query = """
        SELECT 
            c.customer_id, c.first_name, c.last_name, c.email,
            r.rental_id, r.rental_date, r.return_date, r.inventory_id, r.staff_id,
            p.payment_id, p.amount, p.payment_date, p.staff_id AS payment_staff_id
        FROM customer c
        LEFT JOIN rental r ON c.customer_id = r.customer_id
        LEFT JOIN payment p ON r.rental_id = p.rental_id
        ORDER BY c.customer_id, r.rental_id, p.payment_id
    """
        await cursor.execute(query)
        rows = await cursor.fetchall()
    conn.close()

    customers_dict = {}
    for row in rows:
        cust_id = row["customer_id"]
        if cust_id not in customers_dict:
            customers_dict[cust_id] = {
                "customer_id": cust_id,
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "rentals": []
            }
        # Rentals pueden ser None si el cliente no tiene rentals
        if row["rental_id"]:
            # Buscar si el rental ya está agregado
            rentals = customers_dict[cust_id]["rentals"]
            rental = next((r for r in rentals if r["rental_id"] == row["rental_id"]), None)
            if not rental:
                rental = {
                    "rental_id": row["rental_id"],
                    "rental_date": row["rental_date"],
                    "return_date": row["return_date"],
                    "inventory_id": row["inventory_id"],
                    "staff_id": row["staff_id"],
                    "payments": []
                }
                rentals.append(rental)
            # Pagos pueden ser None si el rental no tiene pagos
            if row["payment_id"]:
                payment = {
                    "payment_id": row["payment_id"],
                    "amount": row["amount"],
                    "payment_date": row["payment_date"],
                    "staff_id": row["payment_staff_id"]
                }
                rental["payments"].append(payment)

    return {"customers": list(customers_dict.values())}