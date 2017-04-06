from flask import Flask
from flask import render_template
from flask_cors import CORS, cross_origin
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
CORS(app)

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
    cursor2 = conn.cursor()
    cursor3 = conn.cursor()
    cursor.execute('SELECT "Over_Id",sum("Batsman_Scored")+sum("Extra_Runs") as "Total_Runs" from "ball_by_ball" where "Match_Id"=335988 and "Innings_Id"=2 group by "Over_Id" limit 100;')
    cursor1.execute('SELECT "Over_Id",sum("Batsman_Scored")+sum("Extra_Runs") as "Total_Runs" from "ball_by_ball" where "Match_Id"=335988 and "Innings_Id"=1 group by "Over_Id" limit 100')
    cursor2.execute('select distinct team."Team_Name" from ball_by_ball,team where ball_by_ball."Match_Id"=335988 and "Innings_Id"=1 and ball_by_ball."Team_Batting_Id"=team."Team_Id"')
    cursor3.execute('select distinct team."Team_Name" from ball_by_ball,team where ball_by_ball."Match_Id"=335988 and "Innings_Id"=2 and ball_by_ball."Team_Batting_Id"=team."Team_Id"')
    result = cursor.fetchall()
    result1 = cursor1.fetchall()
    result2 = cursor2.fetchall()[0]
    result3 = cursor3.fetchall()[0]
    list2 = {"Team_One": result2, "Team_Two": result3 ,"Innings1": [{'Over_Id': key, 'Runs': value} for key, value in result], "Innings2": [
        {'Over_Id': key, 'Runs': value} for key, value in result1]}
    records = json.dumps(list2, indent=4)
    cursor.close()
    conn.close()
    return records

@app.route("/iplviz/player")
def player_data():
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute('''SELECT distinct "Player_Name","Dismissal_Type",count("Dismissal_Type") from "player","ball_by_ball" where "Dismissal_Type" not in (' ','run out') and "Bowler_Id"="player"."Player_Id" and "Player_Name"='SK Warne' group by "Player_Name","Dismissal_Type"''')
    playername = cursor.fetchall()
    bowlerStatistics = []
    for i in playername:
        x = {}
        x['Player_Name'] = i[0]
        x['Dismissal_Type'] = i[1]
        x['Count'] = int(i[2])
        bowlerStatistics.append(x)
    cursor.close()
    conn.close()
    return json.dumps(bowlerStatistics)
    
    
if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
