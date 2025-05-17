
## Pasos para ejecutar el proyecto

1. **Ubícate en la carpeta raíz del proyecto**  
   Asegúrate de estar en la carpeta raíz donde se encuentra el archivo `docker-compose.yml`.

2. **Levanta los servicios con Docker Compose**  
   Ejecuta el siguiente comando en la terminal:
   ```bash
   docker-compose up --build
   ```

3. **Sigue las instrucciones de la carpeta `db`**  
   Dentro de la carpeta `db`, encontrarás los scripts necesarios para inicializar la base de datos. Asegúrate de que los archivos SQL (`sakila-schema.sql` y `sakila-data.sql`) estén correctamente configurados y cargados en el contenedor.

4. **Accede a la API**  
   Una vez que los servicios estén corriendo, puedes acceder a la API en `http://localhost:8000`. También puedes explorar la documentación interactiva de la API en:
   - **Swagger UI**: `http://localhost:8000/docs`
   

## Notas adicionales

- Asegúrate de que Docker y Docker Compose estén instalados en tu sistema antes de ejecutar los comandos.
- Si necesitas detener los servicios, utiliza:
  ```bash
  docker-compose down
  ```
```