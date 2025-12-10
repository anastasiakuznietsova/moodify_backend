from fastapi import HTTPException
import base64
import re
import requests
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

def get_access_token():
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post("https://accounts.spotify.com/api/token",
                             headers=headers, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Invalid Spotify credentials")
    return response.json()["access_token"]


def extract_spotify_id(url: str):
    pattern = r"open\.spotify\.com\/track\/([a-zA-Z0-9]+)"
    match = re.search(pattern, url)
    if not match:
        raise ValueError("Invalid Spotify track URL")
    return match.group(1)

def extract_spotify_playlist_id(url: str):
    pattern = r"open\.spotify\.com/playlist\/([a-zA-Z0-9]+)"
    match = re.search(pattern, url)
    if not match:
        raise ValueError("Invalid Spotify track URL")
    return match.group(1)

def get_playlist_tracks_ids(url: str):
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    playlist_id = extract_spotify_playlist_id(url)
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    playlist_info = requests.get(url, headers=headers)
    playlist_info.raise_for_status()
    track_list = playlist_info.json()['items']
    tracks_id_list = []
    for item in track_list:
        track_id = item['track']['id']
        tracks_id_list.append(track_id)
    return tracks_id_list