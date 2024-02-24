import pymongo
import os

password=str(os.environ['MONGO_PASS'])
client=pymongo.MongoClient(f"mongodb+srv://quickstatsbot:{password}@quickstatsbot.vo3ed.mongodb.net/QuickStatsBot?retryWrites=true&w=majority")

def user_id_find(user_id):
  if user_id!='' and user_id!=None:
    collection=client.Users.Streamers
    userid=int(user_id)
    user=collection.find_one({"user_id":userid})
    if user==None:
      user=collection.find_one({"user_id":userid})
    return user
  return None

def user_id_edit(user_id,indata):
    collection=client.Users.Streamers
    userdata=collection.find_one({"user_id":int(user_id)})
    try: test=userdata['spotify_token']
    except: userdata['spotify_token']={}
    userdata['spotify_token']=indata
    collection.replace_one({"user_id": user_id},userdata)
    return True