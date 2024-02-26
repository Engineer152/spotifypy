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
