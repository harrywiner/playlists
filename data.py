import json
from my_types import Playlist
from typing import List, Union


def readJSON(filename: str) -> dict:
    file = open(filename)
    return json.load(file)
    
def readPlaylists(filename: str) -> List[Playlist]:
    file = open(filename)
    
    playlists: List[Playlist] = []
    for obj in json.load(file)["playlists"]:
        items=[item["track"] for item in obj["items"]]
        del obj["items"]
        playlists.append(Playlist(items=items, **obj))
    return playlists
   

def getCursor() -> Union[int, int]:
    file = open("cursor.json")
    blob = json.load(file)
    return blob["currentPlaylist"], blob["currentTrack"]

def setCursor(playlistNo: int, trackNo: int):
    with open('cursor.json', 'w') as outfile:
        outfile.write(json.dumps({ "currentPlaylist": playlistNo, "currentTrack": trackNo}))