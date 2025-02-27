import pickle
import streamlit as st
import spotipy
import gdown
import os
from spotipy.oauth2 import SpotifyClientCredentials

# --- Google Drive File Download ---
drive_link = "https://drive.google.com/uc?id=1FMLaMc0eZSgfBCvm6f_SUTAksPXoDU5u"
similarity_file = "similarity.pkl"

# Ensure the file is downloaded only once
if not os.path.exists(similarity_file):
    st.info("Downloading similarity file from Google Drive...")
    gdown.download(drive_link, similarity_file, quiet=False)

# --- Spotify API Setup ---
CLIENT_ID = "c08ada171c2d4ed099cd1c6d354e10d9"
CLIENT_SECRET = "a27579e704d749658d31808b4cbcff75"

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []

    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters

# --- Streamlit UI ---
st.header('Music Recommender System')

# Load Data
music = pickle.load(open('df', 'rb'))
similarity = pickle.load(open(similarity_file, 'rb'))

music_list = music['song'].values
selected_song = st.selectbox("Type or select a song from the dropdown", music_list)

if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_song)
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(recommended_music_names[i])
            st.image(recommended_music_posters[i])
