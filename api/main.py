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
@app.get("/actors")
def get_all_actors():
    cursor.execute("SELECT * FROM actor")
    actors = cursor.fetchall()
    return {"actors": actors}

# Endpoint 2: Obtener todas las películas
@app.get("/movies")
def get_all_movies():
    cursor.execute("SELECT * FROM film")
    movies = cursor.fetchall()
    return {"movies": movies}

# Endpoint 3: Obtener todos los clientes
@app.get("/customers")
def get_all_customers():
    cursor.execute("SELECT * FROM customer")
    customers = cursor.fetchall()
    return {"customers": customers}