from googleapiclient.discovery import Resource
from auth import getAuth
from playlists import insertToPlaylist, searchSong, createPlaylist
from data import readJSON, readPlaylists, getCursor, setCursor
from schedule import calculateCosts, playlistCost, trackCost

def main():
    data = readJSON("data/playlists.json")
    youtube = getAuth()
    if not youtube:
        raise "Authentication Failed!"
    
    playlistId = createPlaylist(data["name"], youtube, data["description"] )
    
    for song in data["items"]:
        songId = searchSong(song["track"]["trackName"], song["track"]["artistName"], youtube)
        insertToPlaylist(songId, playlistId, youtube)
    

if __name__ == "__main__":
    # youtube = getAuth()
    
    # if not youtube:
    #     raise "Authentication Failed!"
    playlists = readPlaylists("data/playlists.json")

    done = False
    count = 0
    while (not done):
        print(f"Iteration: {count}")
        quota_remaining = 10000
        broken = False
        playlistNo, trackNo = getCursor()
        for pIndex in list(range(playlistNo, len(playlists))): 
            playlist = playlists[pIndex]
            if playlist.cost <= quota_remaining and not broken:
                print(f"Playlist {pIndex} {playlist.name} remaining: {quota_remaining} \n Starting at: {trackNo}")
                
                # playlistId = createPlaylist(playlist.name, playlist.description, youtube)
                quota_remaining -= playlist.cost
                for tIndex, track in enumerate(playlist.items[trackNo:]):
                    if track.cost <= quota_remaining:
                        # resourceId = searchSong(track.trackName, track.artistName, youtube)
                        # insertToPlaylist(resourceId, playlistId, youtube)
                        quota_remaining -= track.cost
                        print(f"Track[{tIndex + trackNo}]: {track.trackName}")
                    else: 
                        broken = True
                        setCursor(pIndex, tIndex)
                        count += 1
                        break
                        
                trackNo = 0

            elif not broken:
                setCursor(pIndex, 0)
                print(f"ran out with {quota_remaining} left")
                broken = True
                count += 1
                break
        if not broken:
            setCursor(int(len(playlists)), 0)
            done = True
    print(f"Simulation done after: {count} iterations")