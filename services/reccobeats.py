from fastapi import HTTPException
import requests

from services.genius import get_genius_lyrics
from services.spotify import get_access_token
from utils.http_utils import request_with_retry


def get_track_features(track_id: str):
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    try:
        track_url = f"https://api.spotify.com/v1/tracks/{track_id}"
        track_res = requests.get(track_url, headers=headers)
        track_res.raise_for_status()
        track_data = track_res.json()
    except:
        raise HTTPException(status_code=500, detail="Could not fetch Spotify track data")

    explicit = int(track_data.get("explicit", 0))
    length_sec = track_data.get("duration_ms", 0) // 1000
    title = track_data.get("name")
    artist = track_data.get("artists")[0].get("name")
    primary_artist_id = track_data["artists"][0]["id"]
    try:
        artist_url = f"https://api.spotify.com/v1/artists/{primary_artist_id}"
        artist_res = requests.get(artist_url, headers=headers)
        artist_res.raise_for_status()
        artist_data = artist_res.json()
    except:
        raise HTTPException(status_code=500, detail="Could not fetch Spotify artist data")

    genre = artist_data["genres"][0] if len(artist_data["genres"])>0 else None

    try:
        reccobeats_track_url = f"https://api.reccobeats.com/v1/track?ids={track_id}"
        beat_headers = {'Accept': 'application/json'}

        reccobeats_track_res = request_with_retry(reccobeats_track_url, headers=beat_headers)
        reccobeats_track_res.raise_for_status()

        payload = reccobeats_track_res.json()

        content = payload.get("content", [])
        if not content:
            print(f"Warning: Track {track_id} not found in ReccoBeats database. Skipping.")
            return None

        reccobeats_track_id = content[0]["id"]

        features_url = f"https://api.reccobeats.com/v1/track/{reccobeats_track_id}/audio-features"
        features_res = request_with_retry(features_url, headers=beat_headers)
        features_res.raise_for_status()
        features_data = features_res.json()

    except Exception as e:
        print(f"Error fetching ReccoBeats data for {track_id}: {e}")
        return None

    lyrics = get_genius_lyrics(title, artist)

    feature_dict = {
        "Title": title,
        "Artist": artist,
        "Explicit": explicit,
        "Length": length_sec,
        "Genre": genre,
        "Key": features_data.get("key"),
        "Tempo": features_data.get("tempo"),
        "Loudness_db": features_data.get("loudness"),
        "Time_signature": features_data.get("time_signature") if features_data.get("time_signature") else '4/4',  #usually a default, but user may need to clarify this one lmao
        "Energy": features_data.get("energy"),
        "Danceability": features_data.get("danceability"),
        "Positiveness": features_data.get("valence"),
        "Speechiness": features_data.get("speechiness"),
        "Liveness": features_data.get("liveness"),
        "Acousticness": features_data.get("acousticness"),
        "Instrumentalness": features_data.get("instrumentalness"),
        "text": lyrics
    }
    return feature_dict