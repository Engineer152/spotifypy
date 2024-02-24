import pymongo
import os

password=str(os.environ['MONGO_PASS'])
client=pymongo.MongoClient(f"mongodb+srv://quickstatsbot:{password}@quickstatsbot.vo3ed.mongodb.net/QuickStatsBot?retryWrites=true&w=majority")

def user_find(user_name):
  collection=client.Users.Streamers
  user=collection.find_one({"user_name":user_name})
  return user

def user_id_find(user_id):
  if user_id!='' and user_id!=None:
    collection=client.Users.Streamers
    userid=int(user_id)
    user=collection.find_one({"user_id":userid})
    if user==None:
      user=collection.find_one({"user_id":str(userid)})
    return user
  return None

def user_id_edit(user_id,data):
    collection=client.Users.Streamers
    data=user_id_find(user_id)
    try: test=data['spotify_token']
    except: data['spotify_token']={}
    data['spotify_token']=data
    collection.replace_one({"user_id": user_id},data)
    return True