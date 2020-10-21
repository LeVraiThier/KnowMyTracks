import requests
import base64
import json
import pymongo
import spotipy.util as util
from secrets import *


def retrieveRecentlyPlayed():#call to spotify API to retrieve the 50 last tracks played and return them as <class 'str'>
    token = util.prompt_for_user_token(username=USERNAME, scope=SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
    response =requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50", 
                        headers={
                            "Content-Type":"application/json", 
                            "Authorization":"Bearer "+token
                        })
    json_response = response.json()
    return json.dumps(json_response)

def checkTrackInDB(col, track):
    timestamp=track["played_at"]
    if col.count_documents({ 'played_at': timestamp }, limit = 1):
        return True
    return False

def insertTracksToMongo(col):
    ex=json.loads(retrieveRecentlyPlayed())
    for i in range(len(ex["items"])):
        track=ex["items"][i]
        if not checkTrackInDB(col,track):   
            col.insert_one(track)

def mongoConnexion():
    client = pymongo.MongoClient('your-mongo-connection')
    dbList=client.list_database_names()
    if 'your-db' in dbList:
        db=client['your-db']
    colList=db.list_collection_names()
    if 'your-collection' in colList:
        col=db['your-collection']

    return db

def main():
    mongoDb=mongoConnexion()
    mongoCol=mongoConnexion()['your-collection']
    insertTracksToMongo(mongoCol)
    mongoDb.close()
    
main()