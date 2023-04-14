import argparse
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

logger = logging.getLogger('examples.add_tracks_to_playlist')
logging.basicConfig(level='DEBUG')
scope = 'playlist-modify-public'
# path="./.spotify_caches/eca9ee78-0dbb-48e8-bec1-25b169667d43"
path=os.environ['USER']

def refresh(auth_manager,cache_handler):
  with open(path,'r') as file:
    for row in file:
      row['access_token']=auth_manager.refresh_access_token(cache_handler.get_cached_token['refresh_token'])
      with open(path,'w') as file:
        file.write(str(row))
        file.close()
  return auth_manager

# def get_args():
#     parser = argparse.ArgumentParser(description='Adds track to user playlist')
#     parser.add_argument('-t', '--tids', action='append',
#                         required=True, help='Track ids')
#     parser.add_argument('-p', '--playlist', required=True,
#                         help='Playlist to add track to')
#     return parser.parse_args()

def add_track(playlist,trackid):
    trackid=str(trackid)
    # args = get_args()
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=path)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
      refresh(auth_manager,cache_handler)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    sp.playlist_add_items(playlist_id=playlist,items=[trackid],position=1)