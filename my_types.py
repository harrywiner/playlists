from typing import List, Optional
from pydantic import BaseModel

class Track(BaseModel):
    trackName: str
    artistName: str
    albumName: str
    trackUri: str
    cost: int = 150

class Playlist(BaseModel):
    name: str
    lastModifiedDate: str
    items: List[Track]
    description: Optional[str]
    numberOfFollowers: int
    cost: int = 50
