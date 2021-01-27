# Actividad 3. Bases de datos de grafos

### Equipo 5

- [Daniela Vignau León (A01021698)](https://github.com/dvigleo)
- [Cristopher Alan Cejudo Machuca (A01025468)](https://github.com/ccejudo)
- [Héctor Alexis Reyes Manrique (A01339607)](https://github.com/hreyesm)

## Contenido

  - [Contenido](#contenido)
  - [Descripción del problema](#descripción-del-problema)
  - [Definición de la base de datos](#definición-de-la-base-de-datos)
  - [Configuración y uso](#configuración-y-uso)
  - [Consultas](#consultas)


## Descripción del problema

Haciendo uso del DBMS no relacional Neo4j, se programó un script en Python para poder ejecutar 3 distintas queries sobre la base de datos de _Pokec_. Pokec es la red social más popular de Eslovaquia.
El dataset descargado contiene 1,632,803 nodos y 30,622,564 aristas que describen las relaciones de amistad que tienen dos usuarios que además, a su vez, tienen un conjunto de atributos (59).

## Definición de la base de datos


## Configuración y uso
1. Clonar el repositorio ```https://github.com/tec-csf/tc3041-actividad-3-invierno-2021-eq5.git```
2. Crear un contenedor de Docker con la imagen de Neo4j
```
docker run --name=neo4j -m=4g --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data --volume=$HOME/neo4j/import:/import     --env=NEO4J_AUTH=none neo4j
```
3. Una vez creado el contenedor, acceder al URL http://localhost:7474
4. Crear un archivo ```.env``` y almacenar el URL con la ubicación de la conexión a la base de datos
5. *En la aplicación de Neo4j Desktop ejecutar el siguiente comando para cargar la base de datos:
```
$ bin/neo4j-admin import \
--mode csv \
--database neo4j \
--nodes nodes-header.csv,new-soc-pokec-profiles.csv \
--relationships relation-header.csv,new-soc-pokec-relationships.csv
```
6. Una vez importados los datos, se podrá ejecutar el comando ```python3 main.py``` para correr el programa principal y ejecutar las consultas

## Consultas
