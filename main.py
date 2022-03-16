from googleapiclient.discovery import Resource
from auth import getAuth
from playlists import insertToPlaylist, searchSong, createPlaylist
from data import readJSON, readPlaylists, getCursor, setCursor
from schedule import calculateCosts, playlistCost, trackCost

def main():
    youtube = getAuth()
    
    if not youtube:
        raise "Authentication Failed!"
    playlists = readPlaylists("data/playlists.json")
    quota_remaining = 10000
    broken = False
    playlistNo, trackNo = getCursor()
    try:
        for pIndex in list(range(playlistNo, len(playlists))): 
            playlistNo = pIndex
            playlist = playlists[pIndex]
            if playlist.cost <= quota_remaining and not broken:
                print(f"Playlist {pIndex} {playlist.name} remaining: {quota_remaining} \n Starting at: {trackNo}")
                
                playlistId = createPlaylist(playlist.name, playlist.description, youtube)
                quota_remaining -= playlist.cost
                for tIndex, track in enumerate(playlist.items[trackNo:]):
                    trackNo += 1
                    if track.cost <= quota_remaining:
                        resourceId = searchSong(track.trackName, track.artistName, youtube)
                        insertToPlaylist(resourceId, playlistId, youtube)
                        quota_remaining -= track.cost
                        print(f"Track[{trackNo}]: {track.trackName}")
                    else: 
                        broken = True
                        setCursor(pIndex, tIndex)
                        break
                        
                trackNo = 0

            elif not broken:
                setCursor(pIndex, 0)
                print(f"ran out with {quota_remaining} left")
                broken = True
                break
        if not broken:
            setCursor(int(len(playlists)), 0)
    except:
        print(f"Exception occurred on {playlistNo}, {trackNo}")
        setCursor(playlistNo, trackNo)

if __name__ == "__main__":
    main()