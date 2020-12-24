import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import itertools
from pprint import pprint
#import asyncio


scope = "user-library-read playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
sp = spotipy.Spotify()
playlist_name = input("name your playlist: ")
playlist_description = input("give it a description!\n")


user = sp.current_user()
user_id = user['id']

def get_liked_songs():
    results = sp.current_user_saved_tracks()
    liked_songs = results['items']
    while results['next']:
        results = sp.next(results)
        liked_songs.extend(results['items'])
    return liked_songs

def get_playlist_id(user_id, playlist_name):
    all_playlists = sp.user_playlists(user_id)
    library_id = ''
    library_playlist = None
    found = False
    while all_playlists['next']:
        for playlist in all_playlists['items']:
            if playlist['owner']['id'] == user_id:
                # print(playlist['name'].lower(), playlist_name.lower())
                if playlist['name'].lower() == playlist_name.lower():
                    library_id = playlist['id']
                    found = True
        if found:
            print('Found your playlist!')
            break
        all_playlists = sp.next(all_playlists)


    if library_id == '':
        library_playlist = sp.user_playlist_create(user_id,playlist_name, public=True, collaborative=False, description=playlist_description)
        library_id = library_playlist['id']
    
    return library_id, found


liked_songs = get_liked_songs()
library_id, playlist_exists = get_playlist_id(user_id, playlist_name)


# songs_gen = (song['track']['uri'].split(":")[-1] for song in songs)
song_uri_lst = [song['track']['uri'].split(":")[-1] for song in liked_songs]
print(len(song_uri_lst))

it = iter(song_uri_lst)
while True:
    chunk = tuple(itertools.islice(it, 15))
    if not chunk:
        # sp.playlist_add_items(library_id,)
        break
    # if playlist_exists:
    #     sp.playlist_replace_items(library_id, chunk)
    # else:
    sp.playlist_add_items(library_id, chunk)  

print("done!")