import streamlit as st
from confluent_kafka import Producer
import json
import hashlib
import time
import pycurl
from io import BytesIO

tmdb_api_key = "be8b281445512ada66653c82f997e3d3"
musixmatch_api_key = "4f0b571d5a3b4b0f63b38ef98b084677"

p = Producer({'bootstrap.servers': 'localhost:9092'})

def acked(err, msg):
    if err is not None:
        st.error(f"Failed to deliver message: {err}")
    else:
        st.success(f"Message produced to {msg.topic()} [{msg.partition()}]")

# TMDb API Request Function
def fetch_tmdb_data(api_key, movie_name):
    query = movie_name.replace(" ", "%20")
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
    
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.SSL_VERIFYPEER, 0)
    c.perform()
    c.close()
    
    data = json.loads(buffer.getvalue().decode('utf-8'))
    p.produce('movies_topic', json.dumps(data).encode('utf-8'), callback=acked)
    return data

# Musixmatch API Request Function
def fetch_musixmatch_data(api_key, song_name):
    query = song_name.replace(" ", "%20")
    url = f"https://api.musixmatch.com/ws/1.1/track.search?q_track={query}&apikey={api_key}&page_size=10&page=1&s_track_rating=desc"
    
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.SSL_VERIFYPEER, 0)
    c.perform()
    c.close()
    
    data = json.loads(buffer.getvalue().decode('utf-8'))
    p.produce('music_topic', json.dumps(data).encode('utf-8'), callback=acked)
    return data

# Streamlit UI
st.set_page_config(page_title="Movies and Music API Fetcher", page_icon=":movie_camera:", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main {
        background-color: #000000;
        color: #ffffff;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #800080;
    }
    label {
        color: #0000ff;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>Movies and Music API Fetcher</h1>", unsafe_allow_html=True)

movie_name = st.text_input("Enter the movie name")
song_name = st.text_input("Enter the song name")

if st.button("Send Movie Data"):
    if tmdb_api_key and movie_name:
        fetch_tmdb_data(tmdb_api_key, movie_name)
        p.flush()
    else:
        st.error("Please provide both TMDb API key and movie name")

if st.button("Send Song Data"):
    if musixmatch_api_key and song_name:
        fetch_musixmatch_data(musixmatch_api_key, song_name)
        p.flush()
    else:
        st.error("Please provide both Musixmatch API key and song name")
