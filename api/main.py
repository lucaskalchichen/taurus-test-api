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
@app.get("/v1/actors")
def get_all_actors():

    cursor.execute("SELECT * FROM film ")
    movies = cursor.fetchall()
    
    cursor.execute("SELECT * FROM film_actor")
    film_actors = cursor.fetchall()

    cursor.execute("SELECT * FROM actor")
    actors = cursor.fetchall()


    for actor in actors:
        actor["movies"] = []
        for film_actor in film_actors:
            if film_actor["actor_id"] == actor["actor_id"]:
                for movie in movies:
                    if movie["film_id"] == film_actor["film_id"]:
                        actor["movies"].append(movie)
    
    return {"actors": actors}

# Endpoint 2: Obtener todas las películas
@app.get("/v1/movies")
def get_all_movies():
    
    cursor.execute("SELECT * FROM film ")
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
    return {"customers": customers}


# Endpoint 4: Obtener todos los actores
@app.get("/v1/actors")
def get_all_actors():

    cursor.execute("SELECT * FROM film ")
    movies = cursor.fetchall()
    
    cursor.execute("SELECT * FROM film_actor")
    film_actors = cursor.fetchall()

    cursor.execute("SELECT * FROM actor")
    actors = cursor.fetchall()


    for actor in actors:
        actor["movies"] = []
        for film_actor in film_actors:
            if film_actor["actor_id"] == actor["actor_id"]:
                for movie in movies:
                    if movie["film_id"] == film_actor["film_id"]:
                        actor["movies"].append(movie)
    
    return {"actors": actors}

# Endpoint 5: Obtener todas las películas
@app.get("/v1/movies")
def get_all_movies():
    
    cursor.execute("SELECT * FROM film ")
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
            

# Endpoint 3: Obtener todos los clientes
@app.get("/v1/customers")
def get_all_customers():
    cursor.execute("SELECT * FROM customer")
    customers = cursor.fetchall()
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