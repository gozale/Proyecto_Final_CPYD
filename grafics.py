import streamlit as st
import pandas as pd
import pymongo
from bson.json_util import dumps
import plotly.express as px

# Conexión a la base de datos MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['ProyectoCPYD']

# Funciones para obtener datos de MongoDB y convertirlos en DataFrames de Pandas
def get_movies_data():
    collection = db['movies']
    data = list(collection.find())  # Convertir el cursor a lista
    df = pd.json_normalize(data, 'results', errors='ignore', meta=['page', 'total_pages', 'total_results'])
    return df

def get_music_data():
    collection = db['music']
    data = list(collection.find())  # Convertir el cursor a lista
    # Normalizar los datos en 'track_list'
    track_list_data = []
    for entry in data:
        if 'message' in entry and 'body' in entry['message'] and 'track_list' in entry['message']['body']:
            track_list_data.extend(entry['message']['body']['track_list'])
    df = pd.json_normalize(track_list_data, errors='ignore')
    return df

# Cargar los datos
movies_df = get_movies_data()
music_df = get_music_data()

# Aplicación Streamlit
st.title("Análisis de la base de datos 'ProyectoCPYD'")

# Selección de colección
option = st.selectbox(
    'Seleccione la colección que desea analizar',
    ('movies', 'music')
)

if option == 'movies':
    st.header("Análisis de la colección 'movies'")
    
    st.subheader("Distribución de los votos")
    fig = px.histogram(movies_df, x='vote_average', nbins=20)
    st.plotly_chart(fig)

    st.subheader("Películas más populares")
    popular_movies = movies_df[['title', 'popularity']].sort_values(by='popularity', ascending=False).head(10)
    st.table(popular_movies)

elif option == 'music':
    st.header("Análisis de la colección 'music'")
    
    st.subheader("Distribución de la puntuación de las canciones")
    fig = px.histogram(music_df, x='track.track_rating', nbins=20)
    st.plotly_chart(fig)

    st.subheader("Canciones más populares")
    popular_tracks = music_df[['track.track_name', 'track.num_favourite']].sort_values(by='track.num_favourite', ascending=False).head(10)
    st.table(popular_tracks)
