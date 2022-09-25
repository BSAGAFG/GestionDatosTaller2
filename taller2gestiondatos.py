# -*- coding: utf-8 -*-
"""Taller2GestionDatos.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kHOnN9m6RoEynq4XqXzlnDVagA3FmsfQ

# Taller 2 materia Gestion de datos 

##Materia:        Materia Gestion de Datos
##Docente:        Fabian Peña
##Presentado por: Norbey Marin
##				Bryan Leonardo Figueredo

###Descripcion de la coleccion de datos:

####Este dataset contiene el listado de peliculas desde su inicio hasta el año 2015, donde se tiene un detalle de los generos de las peliculas, el año de realease o lanzamiento, los directores, escritoes, titulo de las peliculas, cantidad de premios ganados y puntuacion de la critica entre otros datos.

####Seleccionamos este dataset ya que es posible generar una variedad de preguntas que pueden ayudar a las empresas de streaming a colocar en sus plataformas las peliculas en un orden de acuerdo a los criterios seleccionados por un cliente en particular.

###Instalando frameworks requeridos
"""

!pip install pymongo[srv]
!pip install pandas-gbq
!pip install db-dtypes
!pip install --upgrade google-cloud-bigquery

"""###Importando librerias requeridas"""

from datetime import datetime
import pymongo
import pandas as pd
import json
import matplotlib.pyplot as plt
from google.cloud import bigquery
from google.oauth2 import service_account
import numpy as np

"""###Definiendo la conexion con la BD y la coleccion seleccionada"""

DB_NAME = "sample_mflix"
COLLECTION = "movies"

client = pymongo.MongoClient("mongodb+srv://BSAGA:Bryanna@cluster0.6ae8ybq.mongodb.net/?retryWrites=true&w=majority", server_api = pymongo.server_api.ServerApi('1'))

db = client[DB_NAME]

col = db[COLLECTION]

lenguajes = col.distinct("genres")
print(lenguajes)

"""##Pregunta No 1: ¿Muestre la tendencia de peliculas producidas por USA a partir del año 2000?

###Traemos solo la data respectiva de la consulta:
"""

datoUSA = db.movies.find({"year": {"$gte": 2000}, "countries": "USA"},
                         {"_id" : 0, "title": 1,"year": 1, "countries" : "USA"})
df1 = pd.json_normalize(datoUSA)

print(df1[:5])

"""###Agrupando los datos por pais y año para alistarlos en la subida a bigquery"""

df1["count"] = 1
df1_grouped = df1.groupby(["year", "countries"]).agg({"count": "sum"}).reset_index()
df1_grouped.sample(16).sort_values(by=['year'], ascending=True)

df1_grouped['year'].dtype

df1_grouped['countries'] = df1_grouped['countries'].astype(str)
df1_grouped['countries'].dtype

df1_grouped['count'].dtype

print(df1_grouped)

"""##Pregunta No 2: ¿Como se distribuyen los premios de las 10 peliculas mas ganadoras a partir del año 2000?

###Traemos solo la data respectiva de la consulta:
"""

datoganadores = db.movies.find({"awards.wins" : {"$gte" : 1}, "year": {"$gte": 2000}},
                               {"_id" : 0, "title": 1,"year" : 1, "awards.wins" : 1}).sort("awards.wins",-1);
df2 = pd.json_normalize(datoganadores).rename(columns = {"title": "title", "year": "year", "awards.wins": "wins"})
df2 = df2[['title','year','wins']]

"""##Rta: """

print(df2[:10])

df2['year'].dtype

df2['wins'].dtype

df2['title'] = df2['title'].astype(str)
df2['title'].dtype

"""##Pregunta No 3: ¿Cual es la produccion de peliculas en las que solo han participado USA ó Colombia ó Mexico, a partir del año 2000?

###Espacio para la definicion de funciones usadas para la limpieza y transformacion de los datos consultados
"""

#Funcion para limpiar el campo de año

def castyear(valor):
  valor = str(valor)
  valor = valor[0:4]
  return valor

#Funcion para filtrar las peliculas producidas en un unico pais

def castpais(valor):
  if len(valor) > 1:
      valor = 'Otro'
  else:
      valor = valor[0]
  #valor = valor[0]
  return valor

"""###Traemos solo la data respectiva de la consulta:"""

datopaises = db.movies.find({"$or": [{"countries": "USA"}, {"countries": "Mexico"}, {"countries": "Colombia"}], "year": {"$gte": 2000}},
                            {"_id" : 0, "title": 1, "countries" : 1, "year" : 1}).sort("awards.wins",-1);
df3 = pd.json_normalize(datopaises)
df3 = df3[['title','year','countries']]

"""###Realizando la transformacion de los datos"""

df3['year'] = df3['year'].apply(castyear)
df3['countries'] = df3['countries'].apply(castpais)
df3['year'] = df3['year'].astype(str).astype(int)
print(df3)

df3 = df3.drop(df3[df3['countries']=='Otro'].index) #Eliminando los registros con paises diferentes a los seleccionados

df3["count"] = 1
df3_grouped = df3.groupby(["year", "countries"]).agg({"count": "sum"}).reset_index()

print(df3_grouped)

df3_grouped.sample(5).sort_values(by=['year'], ascending=True)

df3_grouped['year'].dtype

df3_grouped['count'].dtype

df3_grouped['countries'] = df3_grouped['countries'].apply(castpais)
df3_grouped['countries'].dtype

"""##Explorando y verificando la consistencia de los datos previos a la subida a la bodega de datos"""

df1.isnull().sum()

df2.isnull().sum()

df3.isnull().sum()

"""###Cargando los datos a bigQuery"""

credentials = service_account.Credentials.from_service_account_file("./javeriana-dataprep.json", scopes = ["https://www.googleapis.com/auth/cloud-platform"])

client = bigquery.Client(credentials = credentials, project = credentials.project_id)

"""###Cargando la primera tabla con los datos de la respuesta de la pregunta no 1"""

# Creating the job config
job_config = bigquery.LoadJobConfig(
    schema = [
        # Supported datatypes: https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types
        bigquery.SchemaField("year", bigquery.enums.SqlTypeNames.INT64),
        bigquery.SchemaField("countries", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("count", bigquery.enums.SqlTypeNames.INT64)
    ],
    # Drod and re-create table, if exist
    write_disposition = "WRITE_TRUNCATE",
)

BQ_TABLE_NAME = "dataprep.listings_pregunta1_tendencia"

# Sending the job to BigQuery
job = client.load_table_from_dataframe(
    df1_grouped, BQ_TABLE_NAME, job_config = job_config
)

job.result()

# Verifying if table was successfully created or updated
table = client.get_table(BQ_TABLE_NAME)

print("Loaded {} rows and {} columns to {}".format(table.num_rows, len(table.schema), BQ_TABLE_NAME))

query = """SELECT * FROM `javeriana-dataprep.dataprep.listings_pregunta1_tendencia`"""

visualizacion1 = pd.read_gbq(query, credentials = credentials)

print(visualizacion1[:5])

x = np.array(visualizacion1['year'])
y = np.array(visualizacion1['count'])
print(x,y)

plt.plot(x,y)
plt.xlabel('Year')
plt.ylabel('Count')
plt.title('Movies USA Pregunta 1')
plt.show

"""###Cargando la primera tabla con los datos de la respuesta de la pregunta no 2"""

# Creating the job config
job_config = bigquery.LoadJobConfig(
    schema = [
        # Supported datatypes: https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types
        bigquery.SchemaField("title", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("year", bigquery.enums.SqlTypeNames.INT64),        
        bigquery.SchemaField("wins", bigquery.enums.SqlTypeNames.INT64)
    ],
    # Drod and re-create table, if exist
    write_disposition = "WRITE_TRUNCATE",
)

BQ_TABLE_NAME = "dataprep.listings_pregunta2_distribucion"

# Sending the job to BigQuery
job = client.load_table_from_dataframe(
    df2, BQ_TABLE_NAME, job_config = job_config
)

job.result()

# Verifying if table was successfully created or updated
table = client.get_table(BQ_TABLE_NAME)

print("Loaded {} rows and {} columns to {}".format(table.num_rows, len(table.schema), BQ_TABLE_NAME))

query = """SELECT * FROM `javeriana-dataprep.dataprep.listings_pregunta2_distribucion` order by wins desc limit 11"""

visualizacion2 = pd.read_gbq(query, credentials = credentials)

visualizacion2=visualizacion2.drop(visualizacion2.index[[2]])

x = np.array(visualizacion2['title'])
y = np.array(visualizacion2['wins'])
print(x,y)

plt.pie(y, labels=x, autopct="%0.1f %%")
plt.show()

"""###Cargando la primera tabla con los datos de la respuesta de la pregunta no 3"""

# Creating the job config
job_config = bigquery.LoadJobConfig(
    schema = [
        # Supported datatypes: https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types
        bigquery.SchemaField("year", bigquery.enums.SqlTypeNames.INT64),
        bigquery.SchemaField("countries", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("count", bigquery.enums.SqlTypeNames.INT64)
    ],
    # Drod and re-create table, if exist
    write_disposition = "WRITE_TRUNCATE",
)

BQ_TABLE_NAME = "dataprep.listings_pregunta3_produccion3"

# Sending the job to BigQuery
job = client.load_table_from_dataframe(
    df3_grouped, BQ_TABLE_NAME, job_config = job_config
)

job.result()

# Verifying if table was successfully created or updated
table = client.get_table(BQ_TABLE_NAME)

print("Loaded {} rows and {} columns to {}".format(table.num_rows, len(table.schema), BQ_TABLE_NAME))

query = """select * from `javeriana-dataprep.dataprep.listings_pregunta3_produccion3` order by year asc"""

visualizacion3 = pd.read_gbq(query, credentials = credentials)







print(visualizacion3)

data1=visualizacion3[visualizacion3['countries'] == 'USA']
data2=visualizacion3[visualizacion3['countries'] == 'Mexico']
data3=visualizacion3[visualizacion3['countries'] == 'Colombia']
yearusa = np.array(data1['year'])
yearmex = np.array(data2['year'])
yearcol = np.array(data3['year'])
countusa = np.array(data1['count'])
countmex = np.array(data2['count'])
countcol = np.array(data3['count'])

print(yearcol)

fig,ax=plt.subplots(3,1,figsize=(10,8))

ax[0].bar(yearusa,countusa,color="red")
ax[0].legend(["USA"])
ax[1].bar(yearmex,countmex,color="green")
ax[1].legend(["Mexico"])
ax[2].bar(yearcol,countcol,color="yellow")
ax[2].legend(["Colombia"])

"""###Eliminacion de tablas con errores cargados"""

#table_id = "dataprep.listings_pregunta3_produccion2"
#client.delete_table(table_id, not_found_ok=True)  # Make an API request.
#print("Deleted table '{}'.".format(table_id))

