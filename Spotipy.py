import os
import pandas as pd
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException

# Spotify API credentials
CLIENT_ID = "1582c8cdf9274ab0acb38197698e5872"
CLIENT_SECRET = "2aa93af34cd14ed9a27dd445d6afc5cf"

# Spotify Authentication
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = Spotify(auth_manager=auth_manager)

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Playlist mappings
music_dist = {
    0: "609gQW5ztNwAkKnoZplkao",  # Angry
    1: "1KQiNjmLkHeDxkvRqlUYD2",  # Disgusted
    2: "7pYR6iga1Lb7eSuVkQ5uK9",  # Fearful
    3: "37i9dQZF1DXdPec7aLTmlC",  # Happy
    4: "73YDMR8TOzRefDryWf5x0u",  # Neutral
    5: "3c0Nv5CY6TIaRszlTZbUFk",  # Sad
    6: "5xz6sdIm4OLZYlpFntxnwZ"   # Surprised
}

local_music_dist = {
    0: os.path.join(BASE_DIR, "songs/angry.csv"),
    1: os.path.join(BASE_DIR, "songs/disgusted.csv"),
    2: os.path.join(BASE_DIR, "songs/fearful.csv"),
    3: os.path.join(BASE_DIR, "songs/happy.csv"),
    4: os.path.join(BASE_DIR, "songs/neutral.csv"),
    5: os.path.join(BASE_DIR, "songs/sad.csv"),
    6: os.path.join(BASE_DIR, "songs/surprised.csv"),
}

def fetch_playlist_tracks(playlist_id, emotion_code):
    """Fetches Spotify playlist or local CSV."""
    try:
        tracks = sp.playlist_tracks(playlist_id)['items']
        return pd.DataFrame([{
            "Name": item['track']['name'],
            "Album": item['track']['album']['name'],
            "Artist": item['track']['artists'][0]['name']
        } for item in tracks])
    except SpotifyException:
        return pd.read_csv(local_music_dist[emotion_code])

def music_rec(emotion_code):
    """Gets music recommendations."""
    playlist_id = music_dist.get(emotion_code)
    return fetch_playlist_tracks(playlist_id, emotion_code)
