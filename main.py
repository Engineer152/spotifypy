import os
# os.system('pip install pymongo[srv]')
# os.system('pip install uvicorn')
# os.system('pip install spotipy')
# os.system('pip install asgiref')
# os.system('pip install flask-session')
from flask import Flask, session, request, redirect
from flask_session import Session
import spotipy
import uuid
from database import user_id_edit, user_find
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

def update_token(token_path, user_id):
  with open (token_path, 'r') as f:
    # print('LOGIN TOKEN: '+ token_path)
    out = json.load(f)
    user_id_edit(user_id, out)
    f.close()
  return

def get_temp_token(userdata):
  if userdata!=None and ("spotify_token" in userdata):
    temp_path = f'./tokens/{userdata["user_name"].lower()}_token'
    with open (temp_path, 'w') as f:
      json.dump(userdata['spotify_token'],f)
      f.close()
    return temp_path
  return None

def check_file(path,userdata):
  if exists(path):
    return True
  elif "spotify_token" in userdata:
    out = get_temp_token(userdata)
    if out!=None: return True
    else: return False
  else:
    return False

@app.route('/')
def main():
  # Step 1. Assign user_id to session object
  try: user_id = request.args.get("user_id")
  except: user_id = None
  if 'user_id' not in session:
    session['user_id'] = user_id
  if not session.get('uuid'):
    # Step 2. Visitor is unknown, give random ID
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
    # Step 4. Display sign in link when no token
    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)

  # Step 5. Signed in, display data
  spotify = spotipy.Spotify(auth_manager=auth_manager)
  token_path = f'./tokens/{spotify.me()["display_name"].lower()}_token'
  shutil.copyfile(session_cache_path(),token_path)
  # Step 6. Update user token in database
  if session.get("user_id"):
    update_token(token_path, session.get("user_id"))
  # Redirect to QuickStats Website
  return redirect("https://id.twitch.tv/oauth2/authorize?response_type=code&client_id=8avl1worc89wc3rv0q840vo63ndzoa&redirect_uri=https://quickstats.xyz/auth&scope=user:read:follows%20user:read:subscriptions%20user:read:broadcast%20user:read:email%20clips:edit%20channel:read:subscriptions%20moderation:read%20channel:manage:redemptions%20channel:read:redemptions%20channel:manage:broadcast%20moderator:read:followers%20channel:manage:moderators%20moderator:read:chatters%20channel:read:vips%20moderator:manage:announcements%20moderator:manage:shoutouts%20moderator:read:shoutouts%20user:read:blocked_users%20user:manage:blocked_users")

@app.route('/currently_playing')
def currently_playing():
  user = request.args.get("user_name")
  userdata = user_find(user)
  if user != None:
    path = f'./tokens/{user}_token'
    file_exists = check_file(path,userdata)
    if file_exists:
      cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=path)
      auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
      if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_manager = refresh(auth_manager, cache_handler, path)
        update_token(path,userdata['user_id'])
      spotify = spotipy.Spotify(auth_manager=auth_manager)
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
  userdata = user_find(user)
  if user != None:
    path = f'./tokens/{user}_token'
    file_exists = check_file(path,userdata)
    if file_exists:
      cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=path)
      auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
      if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_manager = refresh(auth_manager, cache_handler, path)
        update_token(path,userdata['user_id'])
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