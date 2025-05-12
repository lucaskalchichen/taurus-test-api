# Instrucciones para cargar la base de datos Sakila

Este documento describe los pasos necesarios para cargar la base de datos Sakila en el contenedor de MySQL.

## Pasos para cargar la base de datos

1. **Conéctate a la shell del contenedor de la base de datos**  
   Ejecuta el siguiente comando en tu terminal para acceder al contenedor de MySQL:
   ```bash
   docker exec -it db bash
   ```

2. **Conéctate a MySQL desde la terminal del contenedor**  
   Una vez dentro del contenedor, ejecuta el siguiente comando para conectarte a MySQL:
   ```bash
   mysql -u root -p
   ```
   Cuando se te solicite, ingresa la contraseña:
   ```
   root
   ```

3. **Carga los scripts de la base de datos**  
   Ejecuta los siguientes comandos uno a la vez para cargar el esquema y los datos de la base de datos Sakila:
   ```sql
   SOURCE /tmp/sakila-schema.sql;
   SOURCE /tmp/sakila-data.sql;
   ```

4. **Verifica que los datos se hayan cargado correctamente**  
   Ejecuta los siguientes comandos uno a la vez para verificar que la base de datos Sakila se haya cargado correctamente:
   ```sql
   USE sakila;
   SHOW FULL TABLES;
   ```

