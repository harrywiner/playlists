import json

from googleapiclient.discovery import Resource

def readJSON(filename: str) -> dict:
    file = open(filename)
    return json.load(file)
    

# Cost: 50
def createPlaylist(title: str, youtube: Resource, description="") -> str:
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

insertPlaylist("API Test", "A test of a mid api", youtube)
searchSong("Althea - 2013 Remaster", "Grateful Dead", youtube)
insertToPlaylist("ZZNZgtj26Fk", "PLMLL7H31r20QHBDg7nHX8sCZq3dq6mRCU", youtube)
"""
