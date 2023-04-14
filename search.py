# shows artist info for a URN or URL
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
import pprint

  # if len(sys.argv) > 1:
  #     search_str = sys.argv[1]
  # else:
  #     search_str = 'Radiohead'

def search_song(message):
  search_str = message
  sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
  result = sp.search(search_str)
  # with open('./dump/result.txt','w') as result_txt:
  #   result_txt.write(str(result['tracks']['items'][0]))
  trackid=result['tracks']['items'][0]['id']
  return trackid