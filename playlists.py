import json
from my_types import Playlist
from typing import List

from googleapiclient.discovery import Resource

# Cost: 50
def createPlaylist(title: str, description: str, youtube: Resource) -> str:
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": title,
            "description": description if description else "",
            "tags": [
              "beans"
            ],
            "defaultLanguage": "en"
          },
          "status": {
            "privacyStatus": "private"
          }
        }
    )
    
    response = request.execute()
    return response["id"]

# searches: {title} {artist} on the main youtube api
# Always takes the first result
# returns the resouce ID
# Cost: 100
def searchSong(title: str, artist: str, youtube: Resource) -> str:
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=f"{title} {artist}"
    )
    response = request.execute()
    # print(f"Found Song: {response["items"][0]["snippet"]["title"]} \n     {response["items"][0]["snippet"]["description"]}")
    return response["items"][0]["id"]["videoId"]


def insertToPlaylist(resourceId: str, playlistId: str, youtube: Resource):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
          "snippet": {
            "playlistId": playlistId,
            "position": 0,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": resourceId
            }
          }
        }
    )
    request.execute()
    

"""
Test methods
youtube = getAuth()

createPlaylist("API Test", "A test of a mid api", youtube)
searchSong("Althea - 2013 Remaster", "Grateful Dead", youtube)
insertToPlaylist("ZZNZgtj26Fk", "PLMLL7H31r20QHBDg7nHX8sCZq3dq6mRCU", youtube)
"""

# def uploadPlaylist(playlist: Playlist, youtube: Resource):
    # playlistId = createPlaylist(playlist.name, playlist.description, youtube)
    # for track in playlist.items:
    #     resourceId = searchSong(track.trackName, track.artistName, youtube)
    #     insertToPlaylist(resourceId, playlistId, youtube)