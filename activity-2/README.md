# Actividad 2. Bases de datos de documentos

### Equipo 5

- [Daniela Vignau León (A01021698)](https://github.com/dvigleo)
- [Cristopher Alan Cejudo Machuca (A01025468)](https://github.com/ccejudo)
- [Héctor Alexis Reyes Manrique (A01339607)](https://github.com/hreyesm)

## Contenido

  - [Descripción del problema](#descripción-del-problema)
  - [Definición de la base de datos](#definición-de-la-base-de-datos)
    - [Patrón de modelado](#patrón-de-modelado)
    - [Colecciones](#colecciones)
  - [Configuración y uso](#configuración-y-uso)
    - [Conexión a MongoDB](#conexión-a-mongodb)
    - [Instalación](#instalación)
      - [Dependencias](#dependencias)
    - [Ejecución del script](#ejecución-del-script)
  - [Consultas](#consultas)
    - [`unwind`](#unwind)
      - [Descripción](#descripción)
      - [Pipeline](#pipeline)
      - [Etapas](#etapas)
    - [`lookup`](#lookup)
      - [Descripción](#descripción-1)
      - [Pipeline](#pipeline-1)
      - [Etapas](#etapas-1)
    - [`graphLookup`](#graphlookup)
      - [Descripción](#descripción-2)
      - [Pipeline](#pipeline-2)
      - [Etapas](#etapas-2)
    - [`geoNear`](#geonear)
      - [Descripción](#descripción-3)
      - [Pipeline](#pipeline-3)
      - [Etapas](#etapas-3)
    - [`facet`](#facet)
      - [Descripción](#descripción-4)
      - [Pipeline](#pipeline-4)
      - [Etapas](#etapas-4)

## Descripción del problema

## Definición de la base de datos

### Patrón de modelado

### Colecciones

## Configuración y uso

### Conexión a MongoDB

### Instalación

#### Dependencias

### Ejecución del script

## Consultas

### `unwind`

#### Descripción

Obtener, en orden descendente, la cantidad de personas de nombre "Murphy" que están inscritas por grupo.

#### Pipeline

```json
[
  { "$match": { "name": "Murphy" } },
  { "$unwind": { "path": "$groups" } },
  { "$group": { "_id": "$groups", "enrolled": { "$sum": 1 } } },
  { "$sort": { "enrolled": -1 } }
]
```

#### Etapas

- `match`: Filtra los documentos por el nombre "Murphy"
- `unwind`: Descompone los documentos obtenidos bajo el criterio "groups"
- `group`: Cuenta el número de personas con el nombre "Murphy" que pertecen a cada uno de los grupos
- `sort`: Ordena los resultados de manera descendente

### `lookup`

#### Descripción

Obtener el promedio de likes de los 10 posts con más likes asociados con el hashtag "semper".

#### Pipeline

```json
[
  {
    "$lookup": {
      "from": "hashtags",
      "localField": "hashtag",
      "foreignField": "_id",
      "as": "hashtagInfo"
    }
  },
  {
    "$replaceRoot": {
      "newRoot": {
        "$mergeObjects": [{ "$arrayElemAt": ["$hashtagInfo", 0] }, "$$ROOT"]
      }
    }
  },
  { "$match": { "name": "semper" } },
  { "$sort": { "likes": -1 } },
  { "$limit": 10 },
  { "$group": { "_id": "$name", "averageLikes": { "$avg": "$likes" } } },
  { "$project": { "_id": 0, "averageLikes": 1 } }
]
```

#### Etapas

- `lookup`: Produce la unión de las colecciones "posts" y "hashtags"
- `replaceRoot`: Extrae el contenido del atributo "hashtagInfo" y lo coloca al mismo nivel de los atributos exteriores
- `match`: Filtra los documentos por el nombre "semper"
- `sort`: Ordena los documentos de mayor a menor número de likes
- `limit`: Limita los resultados a 10
- `group`: Obtiene el promedio de likes
- `project`: Muestra únicamente el atributo "averageLikes"

### `graphLookup`

#### Descripción

Obtener el número total de likes de los posts cuyo autor sea amigo mutuo del usuario con email "quis.diam.luctus@ultricies.net" con mayor número de likes acumulados entre sus posts.

#### Pipeline

```json
[
  { "$match": { "email": "quis.diam.luctus@ultricies.net" } },
  {
    "$graphLookup": {
      "from": "users",
      "startWith": "$friends",
      "connectFromField": "friends",
      "connectToField": "name",
      "as": "ITCs",
      "maxDepth": 2,
      "restrictSearchWithMatch": { "groups": "ITC", "friends": "Marah" }
    }
  },
  { "$project": { "connections": "$ITCs._id" } },
  { "$unwind": { "path": "$connections" } },
  {
    "$lookup": {
      "from": "posts",
      "localField": "connections",
      "foreignField": "user",
      "as": "postInfo"
    }
  },
  { "$sort": { "postInfo.likes": -1 } },
  { "$limit": 1 },
  { "$unwind": { "path": "$postInfo" } },
  { "$group": { "_id": None, "totalLikes": { "$sum": "$postInfo.likes" } } },
  { "$project": { "_id": 0 } }
]
```

#### Etapas

- `match`: Filtra los documentos a partir del correo electrónico "quis.diam.luctus@ultricies.net"
- `graphLookup`: Recopila los amigos del dueño del correo electrónico especificado que pertenecen al grupo ITC y que, además, tienen como amigo al dueño del correo electrónico ("Marah")
- `project`: Obtiene el ID de los amigos anteriormente encontrados
- `unwind`: Descompone los documentos bajo el criterio "connections"
- `lookup`: Realiza la unión de las colecciones "users" y "posts"
- `sort`: Ordena de manera descencente los resultados obtenidos
- `limit`: Limita los resultados a 1 para obtener el documento con mayor número de likes
- unwind: Descompone el documento a partir del criterio "postInfo"
- `group`: Realiza la suma total de likes
- `project`: Muestra únicamente la suma

### `geoNear`

#### Descripción

Obtener la distancia promedio que existe a partir de la coordenada [-77.73, -5.71] tomando como referencia los 56 posts con mayor distancia del punto original cuya fecha de publicación está entre '2021-01-01' y '2020-06-01' y que tienen más de 950 likes.

#### Pipeline

```json
[
  {
    "$geoNear": {
      "near": { "type": "Point", "coordinates": [-77.73, -5.71] },
      "distanceField": "distance"
    }
  },
  {
    "$match": {
      "date": {
        "$lt": datetime(2021, 1, 1, 0, 0, 0, (tzinfo = timezone.utc)),
        "$gte": datetime(2020, 6, 1, 0, 0, 0, (tzinfo = timezone.utc))
      },
      "likes": { "$gt": 950 }
    }
  },
  { "$sort": { "distance": 1 } },
  { "$skip": 50 },
  {
    "$group": { "_id": "distance", "averageDistance": { "$avg": "$distance" } }
  },
  { "$project": { "_id": 0, "averageDistance": 1 } }
]
```

#### Etapas

- `geoNear`: Encuentra la distancia que existe a partir del punto [-77.73, -5.71] con el resto de los documentos en la colección "posts"
- `match`: Filtra los documentos por fecha de publicación (2021-01-01 y 2020-06-01) y por aquellos que tengan más de 950 likes
- `sort`: Ordena los documentos de manera ascendente
- `skip`: En este momento, existen 106 documentos, por lo que se descartan los primeros 50 y se conservan los 56 restantes
- `group`: Computar la distancia promedio en los 50 posts restantes
- `project`: Mostrar únicamente la distancia obtenida

### `facet`

#### Descripción

Obtener para los usuarios con dominios de correo '@elitpretium.edu', '@Nullamsuscipit.edu' y '@eu.net':
            1. Categorización por likes de los posts de los usuarios del grupo ITC (4 grupos)
            2. Categorización por likes de los posts de los usuarios del grupo SATI (5 grupos)
            3. Posts del grupo Lost & Found publicados después de la fecha 2020-01-01
            4. Posts del grupo Becarios ordenado por número de likes descendentemente

#### Pipeline
```json
[
   {
      "$match":{
         "$or":[
            {"email":{"$regex":".+@elitpretium.edu"}},
            {"email":{"$regex":".+@Nullamsuscipit.edu"}},
            {"email":{"$regex":".+@eu.net"}}
         ]
      }
   },
   {
      "$lookup":{
         "from":"posts",
         "localField":"_id",
         "foreignField":"user",
         "as":"post"
      }
   },
   {
      "$unwind":{"path":"$groups"}
   },
   {
      "$facet":{
         "group-ITC":[
            {"$match":{"groups":"ITC"}},
            {"$unwind":{"path":"$post"}},
            {
               "$bucketAuto":{
                  "groupBy":"$post.likes",
                  "buckets":4
               }
            }
         ],
         "group-SATI":[
            {"$match":{"groups":"SATI"}},
            {"$unwind":{"path":"$post"}},
            {
               "$bucketAuto":{
                  "groupBy":"$post.likes",
                  "buckets":5
               }
            }
         ],
         "group-Lost&Found":[
            {"$match":{"groups":"Lost & Found"}},
            {"$unwind":{"path":"$post"}},
            {"$match":{"post.date":{"$gte": ISODate(2020-01-01)}}}
         ],
         "group-Becarios":[
            {"$match":{"groups":"Becarios"}},
            {"$unwind":{"path":"$post"}},
            {"$sort":{"post.likes":-1}}
         ]
      }
   }
]
```

#### Etapas
- match: Encuentra los usuarios con los dominios de correos indicados, haciendo uso de expresiones regulares
- lookup: Realiza la unión de usuarios con sus respectivos posts
- unwind: Separa los usuarios con los grupos que pertece respectivamente
- facet: Realiza un pipeline para cada uno de los 4 requerimientos
  - group-ITC: Agrupa a los usuarios que pertecen al grupo ITC y realiza una categorización de 4 grupos según el número de likes de todos los posts
  - group-SATI: Agrupa a los usuarios que pertecen al grupo SATI y realiza una categorización de 5 grupos según el número de likes de todos los posts
  - group-Lost&Found: Agrupa a los usuarios que pertecen al grupo Lost & Found y muestra únicamente los posts publicados después de la fecha 2020-01-01
  - group-Becarios: Agrupa a los usuarios que pertecen al grupo Becarios y ordena todos los posts de manera descendente según el número de likes
