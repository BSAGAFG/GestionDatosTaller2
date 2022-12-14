# GestionDatosTaller2
Taller 2 materia Gestion de datos 

Materia:        Materia Gestion de Datos

Docente:        Fabian Peña

Presentado por: 
Norbey Marin y Bryan Leonardo Figueredo


Taller No 2


A partir de una de las colecciones de datos de prueba cargadas en MongoDB Atlas
(diferente a la de AirBnB), diseñe una bodega de datos en BigQuery y desarrolle un
ETL que permita leer datos desde MongoDB, transformarlos, agregarlos y
almacenarlos en BigQuery. Tenga en cuenta que debe diseñar 3 tablas que,
dependiendo del contexto de los datos, deben permitir responder preguntas relevantes
para el negocio.

Evite leer de MongoDB la colección completa en una sola query. Cada pregunta de
negocio debe tener una query a MongoDB que permita traer solamente los datos
requeridos para realizar posteriormente la transformaciones y agregaciones requeridas
en Pandas para, finalmente, ser cargadas en BigQuery.
1. Cada subproceso de ETL complementado con su respectiva query de MongoDB
y carga a BigQuery tiene una ponderación en la nota del 25%.
2. El 25% restante está destinado a documentación incluyendo aspectos como:
a. Descripción general de la colección de datos escogida.
b. Definición de las 3 preguntas de negocio que se quieren responder.
c. Visualización de los resultados tras consultar las tablas en BigQuery.
Puede hacerlo desde Python o desde cualquier herramienta que le
permita conectarse a BigQuery y construir visualizaciones (p.e. Power BI
o Tableau).

El dataset seleccionado fue el siguiente:
	DB_NAME = "sample_mflix"
	COLLECTION = "movies"

Este dataset contiene el listado de peliculas desde su inicio hasta el año 2015, donde se tiene un detalle de 
los generos de las peliculas, el año de realease o lanzamiento, los directores, escritoes, titulo de las peliculas, cantidad
de premios ganados y puntuacion de la critica entre otros datos.

Seleccionamos este dataset ya que es posible generar una variedad de preguntas que pueden ayudar a las empresas de streaming a
colocar en sus plataformas las peliculas en un orden de acuerdo a los criterios seleccionados por un cliente en particular.

Pregunta No 1: ¿Muestre la tendencia de peliculas producidas por USA a partir del año 2000?
Pregunta No 2: ¿Como se distribuyen los premios de las 10 peliculas mas ganadoras a partir del año 2000?
Pregunta No 3: ¿Cual es la produccion de peliculas en las que solo han participado USA ó Colombia ó Mexico, a partir del año 2000?

El detalle del proceso realizado para la conexion, extraccion, transformacion y cargue de las respuestas a las preguntas formuladas
se encuentra en el archivo adjunto .py con sus respectivos comentarios.