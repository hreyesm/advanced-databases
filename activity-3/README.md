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
  - [Ejecución de consultas](#ejecucion-de-consultas)
- [Consultas](#consultas)

## Descripción del problema

Utilizando el DBMS orientado a grafos Neo4j, se programó un script en Python para ejecutar tres consultas diferentes en una base de datos modelada a partir de [_soc-pokec_](https://snap.stanford.edu/data/soc-pokec.html), un dataset del proyecto [SNAP](https://snap.stanford.edu/snap/).

## Definición de la base de datos

### Dataset

Pokec es la red social más popular de Eslovaquia. El dataset _soc-pokec_ contiene 1,632,803 nodos (perfiles) y 30,622,564 aristas (relaciones) que describen las relaciones amistosas entre usuarios, cada uno de los cuales tiene un conjunto de 59 atributos. Los perfiles y las relaciones entre ellos están definidas en los archivos [soc-pokec-profiles.txt](https://snap.stanford.edu/data/soc-pokec-relationships.txt.gz) y [soc-pokec-relationships.txt](https://snap.stanford.edu/data/soc-pokec-relationships.txt.gz), respectivamente.

#### _soc-pokec-profiles_

El archivo contiene 59 columnas, separadas por una tabulación, que describen distintos atributos de los perfiles de los usuarios. Algunos ejemplos de atributos son _user_id_, _last_login_, _age_, _eye_color_ y _politics_.

#### _soc-pokec-relationships_

El archivo está compuesto por 2 columnas, separadas por una tabulación, que describen la relación de amistad que existe entre un usuario y otro. Por ejemplo, la fila con _start_id_ = 1 y _end_id_ = 6 indica la relación unidireccional que el usuario con _user_id_ 1 tiene con el usuario con _user_id 6., lo que significa que las relaciones de amistad son dirigidas.

### Esquema de la base de datos

![Esquema](./images/schema.jpg)

## Solución

### Preparación de archivos

El primer paso para resolver el problema fue preparar ambos archivos del dataset para su procesamiento. Para ello, se eliminaron las comas (,) y las comillas dobles (") de los archivos _soc-pokec-profiles_ y _soc-pokec-relationships_ cuando aún estaban en formato TXT con la ayuda del script [remove_quotes.py](remove_quotes.py). Esta preparación fue necesaria, ya que Neo4j, por un lado, requiere que la importación de datos se realice desde archivos CSV, lo que implicaría un conflicto con aquellos registros que contienen comas; y por otro lado, no facilita la inserción de registros con comillas dobles.

Posteriormente, los archivos TXT resultantes fueron convertidos a formato CSV, proceso durante el cual se agregaron los atributos (_headers_) correspondientes. El script [txt_to_csv.py](./txt_to_csv.py) fue útil para llevar a cabo tal tarea.

Por último, para hacer más eficiente la inserción de relaciones en la base de datos, el archivo _soc-pokec-relationships_ se dividió en tres partes. Inicialmente se consideró ejecutar el script [populate_database.py](./populate_database.py) para este propósito; sin embargo, los tiempos de inserción fueron largos. Por eso se decidió insertar los registros en partes desde la aplicación Neo4j Desktop usando los comandos que se encuentran en [populate_database.cypher](./populate_database.cypher).

[DESCRIBIR UN POCO MÁS A DETALLE LA SEGMENTACIÓN DE LOS ARCHIVOS]

### Implementación de la base de datos

1. Desde la aplicación Neo4j Desktop, crear un proyecto y una base de datos con el nombre de «Pokec».
2. Instalar el plugin [Graph Data Science Library](https://neo4j.com/docs/graph-data-science/current/introduction/) desde la aplicación, ya que es necesario para poder ejecutar la [consulta 1](#consulta-1), que involucra el algoritmo de vecinos comunes.
3. Inicializar la base de datos y acceder a Neo4j Browser.
4. Ejectuar el primer comando del archivo [populate_database.cypher](./populate_database.cypher) para cargar los nodos del grafo.
5. Ejecutar el segundo comando del archivo [populate_database.cypher](./populate_database.cypher) para crear un índice y facilitar la inserción de relaciones.
6. Ejecutar los siguientes tres comandos del archivo [populate_database.cypher](./populate_database.cypher) para cargar las relaciones.

_Nota:_ Es imporante esperar a que cada comando termine de ejecutarse para ejecutar el siguiente.

### Ejecución de consultas

Una vez que se han insertado los datos y se ha inicializado la base de datos, se deberán implementar los siguientes pasos:

1. Crear un archivo `.env` y almacenar, en diferentes variables, la URL de conexión, el nombre de usuario y la contraseña necesarios para poder conectarse a la base de datos con el driver de Neo4j para Python.
2. Ejecutar el comando `python3 main.py` para comenzar a ejecutar las consultas.

## Consultas

### Consulta 1

**Descripción**

Obtener el número de amigos que los usuarios con _userID_ 2 y 3 tienen en común. [HACER MÁS DESCRIPTIVO]

**Comando**

 ```
 MATCH (p1:Profile {userID: '3'})
 MATCH (p2:Profile {userID: '2'})
 RETURN gds.alpha.linkprediction.commonNeighbors(p1, p2) AS score
 ```

**Resultados**
 
![Consulta 1](./images/query-1.jpg)

### Consulta 2

**Descripción**

Obtener los atributos _userID_, _gender_ y _AGE_ de los usuarios que trabajan en el mismo campo y que tienen una distancia de 2 a 3 conexiones con respecto al usuario con _userID_ 1.

**Comando**

 ```
 MATCH (p:Profile {userID: '1'})-[*2..3]->(q:Profile)
 WHERE p.I_am_working_in_field = q.I_am_working_in_field
 RETURN q.userID, q.gender, q.AGE
 ```

**Resultados**

![Consulta 2](./images/query-2.jpg)

### Consulta 3

**Descripción**

Obtener el número de usuarios que tienen una relación de amistad mutua, su perfil es público y tienen la misma edad.

**Comando**

 ```
 MATCH (n:Profile)-[:FRIENDS_WITH]->(m:Profile), (n)<-[:FRIENDS_WITH]-(m)
 WHERE n.public = '1' and n.AGE = m.AGE
 RETURN COUNT (*)
 ```
 
 **Resultados**

![Consulta 3](./images/query-3.jpg)
