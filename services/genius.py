import re
from lyricsgenius import Genius
from config import GENIUS_TOKEN

genius = Genius(GENIUS_TOKEN)
genius.verbose = False
genius.remove_section_headers = True
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]

def clean_plain_text(raw: str) -> str:
    text = raw.encode('utf-8').decode('unicode_escape')
    text = re.sub(r'\[.*?\]', ' ', text)
    text = re.sub(r'\(.*?\)', ' ', text)
    text = text.replace("\n", " ")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def get_genius_lyrics(title: str, artist: str):
    try:
        song = genius.search_song(title, artist)
        if song is None or not song.lyrics:
            return None
        return clean_plain_text(song.lyrics)
    except:
        return None