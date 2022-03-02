from typing import List
from my_types import Track, Playlist
from functools import reduce


def calculateCosts(playlist: List[Playlist]) -> int:
    return 50 + 150*len(playlist.items)

def playlistCost() -> int:
    return 50

def trackCost(track: Track) -> int:
    return 150
    