# GestionDatosTaller2
Taller 2 materia Gestion de datos 

Materia:        Materia Gestion de Datos
Docente:        Fabian Peña
Presentado por: Norbey Marin
				Bryan Leonardo Figueredo

Taller clase No 2


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


