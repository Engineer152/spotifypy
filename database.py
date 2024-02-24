import pymongo
import os

password=str(os.environ['MONGO_PASS'])
client=pymongo.MongoClient(f"mongodb+srv://quickstatsbot:{password}@quickstatsbot.vo3ed.mongodb.net/QuickStatsBot?retryWrites=true&w=majority")

def user_id_edit(user_id,indata):
    collection=client.Users.Streamers
    userdata=collection.find_one({"user_id":int(user_id)})
    userdata['spotify_token']=indata
    collection.replace_one({"user_id": int(user_id)},userdata)
    return