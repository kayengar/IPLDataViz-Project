from flask import Flask
from flask import render_template
import json
import psycopg2
import pprint
import os
import sys
import string
import collections
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)

conn_string = "host='localhost' dbname='ipldata-dv' user='postgres'"
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
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    cursor.execute('SELECT "Over_Id",sum("Batsman_Scored")+sum("Extra_Runs") as "Total_Runs" from "ball_by_ball" where "Match_Id"=335987 and "Innings_Id"=2 group by "Over_Id" limit 100;')
    cursor1.execute('SELECT "Over_Id",sum("Batsman_Scored")+sum("Extra_Runs") as "Total_Runs" from "ball_by_ball" where "Match_Id"=335987 and "Innings_Id"=1 group by "Over_Id" limit 100')
    result = cursor.fetchall()
    result1 = cursor1.fetchall()
    list2 = {}
    list2 = {"Innings1": [{'Over_Id': key, 'Runs': value} for key, value in result], "Innings2": [
        {'Over_Id': key, 'Runs': value} for key, value in result1]}
    records = json.dumps(list2, indent=4)
    cursor.close()
    conn.close()
    return records

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
