# Prerequisites
#     pip3 install spotipy Flask Flask-Session
#     // from your [app settings](https://developer.spotify.com/dashboard/applications)
#     export SPOTIPY_CLIENT_ID=client_id_here
#     export SPOTIPY_CLIENT_SECRET=client_secret_here
#     export SPOTIPY_REDIRECT_URI='http://127.0.0.1:8080' // must contain a port
#     // SPOTIPY_REDIRECT_URI must be added to your [app settings](https://developer.spotify.com/dashboard/applications)
#     OPTIONAL
#     // in development environment for debug output
#     export FLASK_ENV=development
#     // so that you can invoke the app outside of the file's directory include
#     export FLASK_APP=/path/to/spotipy/examples/app.py

#     // on Windows, use `SET` instead of `export`
# Run app.py
#     python3 app.py OR python3 -m flask run
#     NOTE: If receiving "port already in use" error, try other ports: 5000, 8090, 8888, etc...
#         (will need to be updated in your Spotify app and SPOTIPY_REDIRECT_URI variable)

import os
# os.system('pip install uvicorn')
# os.system('pip install spotipy')
# os.system('pip install asgiref')
# os.system('pip install flask-session')
from flask import Flask, session, request, redirect
from flask_session import Session
import spotipy
import uuid
from threading import Thread
from add_tracks_to_playlist import add_track
from search import search_song
from os.path import exists
import json
import shutil
import uvicorn
from asgiref.wsgi import WsgiToAsgi

app = Flask('')
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

#USER PATH
# path="./tokens/QuickStatsBot_token"
# path="./.spotify_caches/eca9ee78-0dbb-48e8-bec1-25b169667d43"
path = os.environ['USER']

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
  os.makedirs(caches_folder)


def session_cache_path():
  return caches_folder + session.get('uuid')


def refresh(auth_manager, cache_handler, path):
  with open(path, 'r') as file:
    for row in file:
      row['access_token'] = auth_manager.refresh_access_token(
        cache_handler.get_cached_token['refresh_token'])
      with open(path, 'w') as file:
        file.write(str(row))
        file.close()
  return auth_manager


@app.route('/')
def main():
  if not session.get('uuid'):
    # Step 1. Visitor is unknown, give random ID
    session['uuid'] = str(uuid.uuid4())

  cache_handler = spotipy.cache_handler.CacheFileHandler(
    cache_path=session_cache_path())
  auth_manager = spotipy.oauth2.SpotifyOAuth(
    scope=
    'user-read-currently-playing playlist-modify-private playlist-modify-public playlist-read-private playlist-read-collaborative user-read-currently-playing user-read-playback-state user-read-playback-position user-read-recently-played user-top-read user-library-read user-follow-read',
    cache_handler=cache_handler,
    show_dialog=True)

  if request.args.get("code"):
    # Step 3. Being redirected from Spotify auth page
    auth_manager.get_access_token(request.args.get("code"))
    return redirect('/')

  if not auth_manager.validate_token(cache_handler.get_cached_token()):
    # Step 2. Display sign in link when no token
    auth_url = auth_manager.get_authorize_url()
    return '<h2>Link Spotify to QuickStatsBot<h2>' \
          f'<h2><a href="{auth_url}">Sign in</a></h2>'

  # Step 4. Signed in, display data
  spotify = spotipy.Spotify(auth_manager=auth_manager)
  shutil.copyfile(session_cache_path(),
                  f'./tokens/{spotify.me()["display_name"].lower()}_token')
  return f'<h2>Hi {spotify.me()["display_name"]}</h2>' \
         f'<p>You are now Connected with QuickStats</p>'


@app.route('/currently_playing')
def currently_playing():
  user = request.args.get("user_name")
  if user != None:
    path = f'./tokens/{user}_token'
    file_exists = exists(path)
    if file_exists:
      cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=path)
      auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
      if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_manager = refresh(auth_manager, cache_handler, path)
      spotify = spotipy.Spotify(auth_manager=auth_manager)
      # track = spotify.current_user_playing_track()
      track = spotify.currently_playing()
      print(track)
      if not track is None:
        return track
      return {"error": "No track currently playing."}
    return {"error": "User is not authorized, or logged in."}
  return {"error": "There is an error with the Spotify API."}


@app.route('/recently_played')
def recently_played():
  user = request.args.get("user_name")
  if user != None:
    path = f'./tokens/{user}_token'
    file_exists = exists(path)
    if file_exists:
      cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=path)
      auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
      if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_manager = refresh(auth_manager, cache_handler, path)
      spotify = spotipy.Spotify(auth_manager=auth_manager)
      tracks = spotify.current_user_recently_played(limit=50)
      if not tracks is None:
        return tracks
      return {"error": "No recently played tracks."}
    return {"error": "User is not authorized, or logged in."}
  return {"error": "There is an error with the Spotify API."}


'''
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
'''

app = WsgiToAsgi(app)
# uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")

# def run():
#     app.run(host="0.0.0.0", port=8888)

# def keep_alive():
#     server = Thread(target=run)
#     server.start()

# @app.route('/sign_out')
# def sign_out():
#     try:
#         # Remove the CACHE file (.cache-test) so that a new user can authorize.
#         os.remove(session_cache_path())
#         session.clear()
#     except OSError as e:
#         print ("Error: %s - %s." % (e.filename, e.strerror))
#     return redirect('/')

# @app.route('/playlists')
# def playlists():
#     #path='./.spotify_caches/eca9ee78-0dbb-48e8-bec1-25b169667d43'
#     cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=path)
#     auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
#     if not auth_manager.validate_token(cache_handler.get_cached_token()):
#       auth_manager=refresh(auth_manager,cache_handler)
#     spotify = spotipy.Spotify(auth_manager=auth_manager)
#     return spotify.current_user_playlists()

# @app.route('/devices')
# def devices():
#     #path='./.spotify_caches/eca9ee78-0dbb-48e8-bec1-25b169667d43'
#     cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=path)
#     auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
#     if not auth_manager.validate_token(cache_handler.get_cached_token()):
#       auth_manager=refresh(auth_manager,cache_handler)
#     spotify = spotipy.Spotify(auth_manager=auth_manager)
#     return spotify.devices()

# @app.route('/current_user')
# def current_user():
#     cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=path)
#     auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
#     if not auth_manager.validate_token(cache_handler.get_cached_token()):
#       auth_manager=refresh(auth_manager,cache_handler)
#     spotify = spotipy.Spotify(auth_manager=auth_manager)
#     return spotify.current_user()

# @app.route('/song_request', methods=['GET','POST'])
# def song_request():
#   #<Reformed playlistid='565fUMPIj7mf9XiiCttslu'
#   playlistid='6oOBqSitVLXTFmYbCyXLwj'
#   message=request.data.decode("utf-8")
#   print(str(message))
#   trackid=search_song(message)
#   add_track(playlistid,trackid)
#   out=message+' has been added to playlist.'
#   print(out)
#   return out

# def keep_alive():
#     app.run(threaded=True, port=int(os.environ.get("PORT", os.environ.get("SPOTIPY_REDIRECT_URI", 8080).split(":")[-1])))
