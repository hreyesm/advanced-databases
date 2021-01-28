# Actividad 3. Bases de datos orientadas a grafos

### Equipo 5

- [Daniela Vignau León (A01021698)](https://github.com/dvigleo)
- [Cristopher Alan Cejudo Machuca (A01025468)](https://github.com/ccejudo)
- [Héctor Alexis Reyes Manrique (A01339607)](https://github.com/hreyesm)

## Contenido

  - [Descripción del problema](#descripción-del-problema)
  - [Definición de la base de datos](#definición-de-la-base-de-datos)
    - [Dataset](#dataset)
      - [_soc-pokec-profiles_](#soc-pokec-profiles)
      - [_soc-pokec-relationships_](#soc-pokec-relationships)
    - [Esquema de la base de datos](#esquema-de-la-base-de-datos)
  - [Solución](#solución)
    - [Preparación de archivos](#preparación-de-archivos)
    - [Implementación de la base de datos](#implementación-de-la-base-de-datos)
  - [Consultas](#consultas)

## Descripción del problema

Utilizando el DBMS orientado a grafos Neo4j, se programó un script en Python para ejecutar tres consultas diferentes en una base de datos modelada a partir de [_soc-pokec_](https://snap.stanford.edu/data/soc-pokec.html), un dataset del proyecto [SNAP](https://snap.stanford.edu/snap/). Pokec es la red social más popular de Eslovaquia.

## Definición de la base de datos

### Dataset

El dataset _soc-pokec_ contiene 1,632,803 nodos (perfiles) y 30,622,564 aristas (relaciones) que describen las relaciones amistosas entre usuarios, cada uno de los cuales tiene un conjunto de 59 atributos. Los perfiles y las relaciones entre ellos están definidas en los archivos [soc-pokec-profiles.txt](https://snap.stanford.edu/data/soc-pokec-relationships.txt.gz) y [soc-pokec-relationships.txt](https://snap.stanford.edu/data/soc-pokec-relationships.txt.gz), respectivamente.

#### _soc-pokec-profiles_

[DESCRIPCIÓN]

#### _soc-pokec-relationships_

[DESCRIPCIÓN]

### Esquema de la base de datos

[IMAGEN]

## Solución

### Preparación de archivos

El primer paso para resolver el problema fue preparar ambos archivos del dataset para su procesamiento. Para ello, se eliminaron las comas (,) y las comillas dobles (") de los archivos _soc-pokec-profiles_ y _soc-pokec-relationships_ cuando aún estaban en formato TXT con la ayuda del script [remove_quotes.py](remove_quotes.py). Esta preparación fue necesaria, ya que Neo4j, por un lado, requiere que la importación de datos se realice desde archivos CSV, lo que implicaría un conflicto con aquellos registros que contienen comas; y por otro lado, no facilita la inserción de registros con comillas dobles.

Posteriormente, los archivos TXT resultantes fueron convertidos a formato CSV, proceso durante el cual se agregaron los atributos (_headers_) correspondientes. El script [txt_to_csv.py](./txt_to_csv.py) fue útil para llevar a cabo tal tarea.

Por último, para hacer más eficiente la inserción de relaciones en la base de datos, el archivo _soc-pokec-relationships_ se dividió en tres partes. Inicialmente se consideró ejecutar el script [populate_database.py](./txt_to_csv.py) para este propósito; sin embargo, los tiempos de inserción fueron largos. Por eso se decidió insertar los registros en partes desde la aplicación Neo4j Desktop.

[DESCRIBIR UN POCO MÁS A DETALLE LA SEGMENTACIÓN DE LOS ARCHIVOS]

### Implementación de la base de datos

[DESCRIBIR PASO A PASO LA CREACIÓN DE LA BASE DE DATOS Y LA INSERCIÓN DE REGISTROS]

## Consultas

1. Obtener la cantidad de amigos que tienen dos usuarios en común [HACER MÁS DESCRIPTIVO]

   ```
   MATCH (p1:Profile {userID: '3'})
   MATCH (p2:Profile {userID: '2'})
   RETURN gds.alpha.linkprediction.commonNeighbors(p1, p2) AS score
   ```

2. Obtener los atributos "userID", "gender" y "AGE" de las personas que trabajan en el mismo campo y que tienen una distancia de 2 a 3 conexiones con respecto al usuario con userID "1"

   ```
   MATCH (p:Profile {userID: '1'})-[*2..3]->(q:Profile)
   WHERE p.I_am_working_in_field = q.I_am_working_in_field
   RETURN q.userID, q.gender, q.AGE
   ```

3. Obtener el número de usuarios que tienen una relación de amistad mútua, su perfil es público y tienen la misma edad

   ```
   MATCH (n:Profile)-[:FRIENDS_WITH]->(m:Profile), (n)<-[:FRIENDS_WITH]-(m)
   WHERE n.public = '1' and n.AGE = m.AGE
   RETURN COUNT (*)
   ```
