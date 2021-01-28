# Actividad 3. Bases de datos orientadas a grafos

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

Utilizando el DBMS orientado a grafos Neo4j, se programó un script en Python para poder ejecutar tres consultas distintas sobre el dataset [soc-pokec](https://snap.stanford.edu/data/soc-pokec.html), del proyecto [SNAP](https://snap.stanford.edu/snap/). Pokec es la red social más popular en Eslovaquia.
El dataset en cuestión contiene 1,632,803 nodos (_Profiles_) y 30,622,564 aristas (_Relationships_) que describen las relaciones amistosas entre usuarios, cada uno de los cuales tiene un conjunto de 59 atributos.

## Definición de la base de datos

Schema

## Solución

El primer paso para la solución del problema fue convertir los datasets, que eran de tipo `.txt`, a archivos `.csv` junto con sus propiedades (headers) correspondientes.

Para facilitar la inserción de datos, se decidió dividir el archivo con las relaciones en 3 distintos nuevos.

- Haciendo uso de neo4j desktop, se ejecutó el comando `LOAD CSV` para añadir los nodos junto con sus relaciones

- Ejecutaron las queries

## Consultas

1. Obtener el número de amigos que tienen en común dos personas

```
MATCH (p1:Profile {userID: '3'})
MATCH (p2:Profile {userID: '2'})
RETURN gds.alpha.linkprediction.commonNeighbors(p1, p2) AS score
```

Resultados

2. Obtener el userID, género y edad de las personas que trabajan en la misma área y que se encuentran a una distancia de 2 a 3 nodos de distancia.

   ```
   MATCH (p:Profile {userID: '1'})-[*2..3]->(q:Profile)
   WHERE p.I_am_working_in_field = q.I_am_working_in_field
   RETURN q.userID, q.gender, q.AGE
   ```

Resultados

3. Obtener el numero de personas que tienen una relación de amistad mútua, que tienen un perfil público y que tengan la misma edad

```
MATCH (n:Profile)-[:FRIENDS_WITH]->(m:Profile), (n)<-[:FRIENDS_WITH]-(m)
WHERE n.public = '1' and n.AGE = m.AGE
RETURN COUNT (*)
```

Resultados
