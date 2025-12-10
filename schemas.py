from pydantic import BaseModel
from typing import Optional

class SongFeatures(BaseModel):
    Title: str
    Artist: str
    Explicit: int
    Length: int
    Genre: Optional[str]
    Key: Optional[int]
    Tempo: Optional[float]
    Loudness_db: Optional[float]
    Time_signature: Optional[str]
    Energy: Optional[float]
    Danceability: Optional[float]
    Positiveness: Optional[float]
    Speechiness: Optional[float]
    Liveness: Optional[float]
    Acousticness: Optional[float]
    Instrumentalness: Optional[float]
    text: Optional[str]