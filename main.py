from googleapiclient.discovery import Resource
from auth import getAuth
from playlists import readJSON, insertToPlaylist, searchSong, createPlaylist

def main():
    data = readJSON("data/playlists.json")
    youtube = getAuth()
    if not youtube:
        raise "Authentication Failed!"
    
    playlistId = createPlaylist(data["name"], youtube, data["description"] )
    
    for song in data["items"]:
        songId = searchSong(song["track"]["trackName"], song["track"]["artistName"], youtube)
        insertToPlaylist(songId, playlistId, youtube)
    
    

# def createPlaylistFromObject(playlist: dict, youtube: Resource):
    
# def estimateCost(playlists)

if __name__ == "__main__":
    main()