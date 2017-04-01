from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'ipldata-dv'
COLLECTION_NAME_MATCH = 'match'
COLLECTION_NAME_BALL = 'ballbyball'
COLLECTION_NAME_PLAYER = 'player'
COLLECTION_NAME_PLAYER_MATCH = 'player_match'
COLLECTION_NAME_SEASON = 'season'
COLLECTION_NAME_TEAM = 'team'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/iplviz/match")
def match_data():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME_MATCH]
    matchValue = collection.find_one({})
    json_dump = []
    for i in matchValue:
        json_dump.append(i)
    json_dump = json.dumps(json_dump, default=json_util.default)
    connection.close()
    return json_dump

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)