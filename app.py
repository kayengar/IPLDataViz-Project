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
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/iplviz/*": {"origins": "http://localhost:3000"}})


conn_string = "host='localhost' dbname='ipldata-dv' user='postgres'"


@app.route("/")
def index():
    return "Hello API"


 #################################Player end points ###############
 #Done 
@app.route("/iplviz/player/playerwickettype/<id>")
def player_data(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    player_id = id
    cursor.execute('SELECT distinct "Player_Name",player."Player_Id","Dismissal_Type",count("Dismissal_Type") from "player","ball_by_ball" where player."Player_Id"='+str(player_id)+' and "Dismissal_Type" not in (\' \',\'run out\') and "Bowler_Id"="player"."Player_Id" group by "Player_Name",player."Player_Id","Dismissal_Type"')
    playername = cursor.fetchall()
    bowlerStatistics = []
    for i in playername:
        x = {}
        x['Player_Name'] = i[0]
        x['Player_Id'] = int(i[1])
        x['Dismissal_Type'] = i[2]
        x['Wickets'] = int(i[3])
        bowlerStatistics.append(x)
    cursor.close()
    conn.close()
    return json.dumps(bowlerStatistics)

#Done
@app.route("/iplviz/player/playerwicket/<id>")
def playerwicket_data(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    player_id=id
    cursor.execute('SELECT distinct "Player_Name",player."Player_Id","Season_Year",count("Dismissal_Type"),ball_by_ball."Season_Id" from ball_by_ball,player,season where player."Player_Id"='+str(player_id)+' and "Dismissal_Type" not in (\' \',\'run out\') and player."Player_Id"=ball_by_ball."Bowler_Id" and season."Season_Id"="ball_by_ball"."Season_Id" group by ball_by_ball."Season_Id","Player_Name",player."Player_Id","Season_Year" order by ball_by_ball."Season_Id"')
    playername = cursor.fetchall()
    bowlerStatistics = []
    for i in playername:
        x = {}
        x['Player_Name'] = i[0]
        x['Player_Id'] = int(i[1])
        x['Season_Year'] = int(i[2])
        x['Wickets'] = int(i[3])
        x['Season_Id'] = int(i[4])
        bowlerStatistics.append(x)
    cursor.close()
    conn.close()
    return json.dumps(bowlerStatistics)

#Done
@app.route("/iplviz/player/strikerate/<id>")
def player_strikerate(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    player_id=id
    cursor.execute('SELECT player."Player_Name",player."Player_Id", (CAST(sum("Batsman_Scored")+sum("Extra_Runs") as FLOAT)/CAST(count(*) as FLOAT))*100 as "Strike Rate",ball_by_ball."Over_Id" from ball_by_ball,player where player."Player_Id"='+str(player_id)+' and player."Player_Id" = ball_by_ball."Striker_Id" group by "Over_Id","Player_Name",player."Player_Id" order by "Over_Id"')
    playername = cursor.fetchall()
    batsmanStatistics = []
    for i in playername:
        x = {}
        x['Player_Name'] = i[0]
        x['Player_Id'] = int(i[1])
        x['Batsman_Scored'] = float(i[2])
        x['Over_Id'] = int(i[3])
        batsmanStatistics.append(x)
    cursor.close()
    conn.close()
    return json.dumps(batsmanStatistics)

#Done
@app.route("/iplviz/player/economyrate/<id>")
def player_economyrate(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    player_id=id
    cursor.execute('SELECT player."Player_Name",player."Player_Id", (CAST(sum("Batsman_Scored")+sum("Extra_Runs") as FLOAT)/CAST(count(*) as FLOAT))*6 as "Strike Rate",ball_by_ball."Over_Id" from ball_by_ball,player where player."Player_Id"='+str(player_id)+' and player."Player_Id" = ball_by_ball."Bowler_Id" group by "Over_Id","Player_Name",player."Player_Id" order by "Over_Id"')
    playername = cursor.fetchall()
    bowlerStatistics = []
    for i in playername:
        x = {}
        x['Player_Name'] = i[0]
        x['Player_Id'] = int(i[1])
        x['Economy_Rate'] = float(i[2])
        x['Over_Id'] = int(i[3])
        bowlerStatistics.append(x)
    cursor.close()
    conn.close()
    return json.dumps(bowlerStatistics)


#Done
@app.route("/iplviz/player/batsmanslogovers/<id>")
def player_batsmanslogovers(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    player_id=id
    cursor.execute('select sum("Batsman_Scored"), player."Player_Name",player."Player_Id",ball_by_ball."Over_Id" from ball_by_ball,player where player."Player_Id"='+str(player_id)+' and "Over_Id" in (15,16,17,18,19,20) and ball_by_ball."Striker_Id"=player."Player_Id" group by ball_by_ball."Over_Id",player."Player_Name",player."Player_Id" order by "Over_Id"')
    playername = cursor.fetchall()
    batsmanStatistics = []
    for i in playername:
        x = {}
        x['Player_Name'] = i[1]
        x['Batsman_Scored'] = int(i[0])
        x['Player_Id'] = int(i[2])
        x['Over_Id'] = int(i[3])
        batsmanStatistics.append(x)
    cursor.close()
    conn.close()
    return json.dumps(batsmanStatistics)

#Done
@app.route("/iplviz/player/bowlerslogovers/<id>")
def player_bowlerslogovers(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    player_id=id
    cursor.execute('SELECT  COUNT(*), player."Player_Name",player."Player_Id",ball_by_ball."Over_Id" from ball_by_ball, player where player."Player_Id"='+str(player_id)+' and ball_by_ball."Over_Id" in (15,16,17,18,19,20) and player."Player_Id" = ball_by_ball."Bowler_Id" and ball_by_ball."Dismissal_Type" IN (\'caught\',\'lbw\',\'stumped\',\'bowled\',\'caught and bowled\') group by ball_by_ball."Over_Id",player."Player_Name",player."Player_Id" order by "Over_Id"')
    playername = cursor.fetchall()
    bowlerStatistics = []
    for i in playername:
        x = {}
        x['Player_Name'] = i[1]
        x['Wickets'] = int(i[0])
        x['Player_Id'] = int(i[2])
        x['Over_Id'] = int(i[3])
        bowlerStatistics.append(x)
    cursor.close()
    conn.close()
    return json.dumps(bowlerStatistics)

#Done
@app.route("/iplviz/player/runsperseason/<id>")
def player_runsperseason(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    player_id=id
    cursor.execute('select sum("Batsman_Scored"), player."Player_Name",player."Player_Id",ball_by_ball."Season_Id","Season_Year" from ball_by_ball,player,season where ball_by_Ball."Season_Id"=season."Season_Id" and player."Player_Id"='+str(player_id)+' and  ball_by_ball."Striker_Id"=player."Player_Id" group by ball_by_ball."Season_Id", player."Player_Name",player."Player_Id","Season_Year" order by ball_by_ball."Season_Id"')
    playername = cursor.fetchall()
    batsmanStatistics = []
    for i in playername:
        x = {}
        x['Player_Name'] = i[1]
        x['Player_Id'] = int(i[2])
        x['Batsman_Scored'] = int(i[0])
        x['Season_Id'] = int(i[3])
        x['Season_Year'] = int(i[4])
        batsmanStatistics.append(x)
    cursor.close()
    conn.close()
    return json.dumps(batsmanStatistics)

@app.route("/iplviz/player/bowlerwicketsseason/<id>")
def player_wicketsseason(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    player_id=32
    cursor.execute('SELECT  COUNT(*), player."Player_Name",player."Player_Id",ball_by_ball."Season_Id","Season_Year" from ball_by_ball, player,season where ball_by_Ball."Season_Id"=season."Season_Id" and player."Player_Id"='+str(player_id)+' and  player."Player_Id" = ball_by_ball."Bowler_Id" and ball_by_ball."Dismissal_Type" IN (\'caught\',\'lbw\',\'stumped\',\'bowled\',\'caught and bowled\') group by ball_by_ball."Season_Id",player."Player_Name",player."Player_Id","Season_Year" order by ball_by_ball."Season_Id"')
    playername = cursor.fetchall()
    bowlerStatistics = []
    for i in playername:
        x = {}
        x['Player_Name'] = i[1]
        x['Wickets'] = int(i[0])
        x['Player_Id'] = int(i[2])
        x['Season_Id'] = int(i[3])
        x['Season_Year'] = int(i[4])
        bowlerStatistics.append(x)
    cursor.close()
    conn.close()
    return json.dumps(bowlerStatistics)

@app.route("/iplviz/player/playerdetails/<id>")
def player_details(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    player_id=id
    cursor.execute('SELECT player."Player_Name",player."Player_Id",player."Country",player."Batting_Hand",player."Bowling_Skill",sum("Batsman_Scored") as "Runs" from player,ball_by_ball where player."Player_Id"='+str(player_id)+' and player."Player_Id" = ball_by_ball."Striker_Id" group by player."Player_Name",player."Player_Id",player."Country",player."Batting_Hand",player."Bowling_Skill"')
    playername = cursor.fetchall()
    cursor2 = conn.cursor()
    cursor2.execute('SELECT  player."Player_Name",player."Player_Id",player."Country",COUNT(*) as "Wickets" from ball_by_ball, player where player."Player_Id"='+str(player_id)+' and player."Player_Id" = ball_by_ball."Bowler_Id" and ball_by_ball."Dismissal_Type" IN (\'caught\',\'lbw\',\'stumped\',\'bowled\',\'caught and bowled\',\'hit wicket\') group by player."Player_Name",player."Player_Id",player."Country"')
    player_details = cursor2.fetchall()
    cursor2.execute('SELECT count(*) from ball_by_ball where "Fielder_Id" ='+str(player_id)+' and "Dismissal_Type" in (\'run out\',\'caught\',\'stumped\',\'caught and bowled\')')
    player1_details = cursor2.fetchall()
    bowlerStatistics = []
    for i in playername:
        x = {}
        x['Player_Name'] = i[0]
        x['Country'] = i[2]
        x['Player_Id'] = int(i[1])
        x['Batsman_Scored'] = int(i[5])
        x['Batting_Style']=i[3]
        x['Bowling_Style']=i[4]
        bowlerStatistics.append(x)
    bowlerStatistics1 =[]
    for j in player_details:
        y = {}
        y['Wickets'] = int(j[3])
        bowlerStatistics1.append(y)
    if not bowlerStatistics1:
        j={}
        j['Wickets']=0
        bowlerStatistics1.append(j)
    bowlerStatistics2 =[]
    for l in player1_details:
        y = {}
        y['Dismissals'] = int(l[0])
        bowlerStatistics2.append(y)
    if not bowlerStatistics2:
        j={}
        j['Dismissals']=0
        bowlerStatistics2.append(j)
    loop =0
    finallist=[]
    while loop < len(bowlerStatistics):
        k={}
        k['Player_Name']=bowlerStatistics[loop]['Player_Name']
        k['Country']=bowlerStatistics[loop]['Country']
        k['Player_Id']=bowlerStatistics[loop]['Player_Id']
        k['Batsman_Scored']=bowlerStatistics[loop]['Batsman_Scored']
        k['Batting_Style']=bowlerStatistics[loop]['Batting_Style']
        k['Bowling_Style']=bowlerStatistics[loop]['Bowling_Style']
        k['Wickets']=bowlerStatistics1[loop]['Wickets']
        k['Dismissals']=bowlerStatistics2[loop]['Dismissals']
        finallist.append(k)
        loop+=1
    cursor.close()
    cursor2.close()
    conn.close()
    return json.dumps(finallist)

@app.route("/iplviz/player/playerradar/<id>")
def player_radar(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    player_id=32
    cursor.execute('SELECT player."Player_Name",player."Player_Id", CAST(sum("Batsman_Scored")+sum("Extra_Runs") as float)/CAST(count(*) as float) * 6 as "Economy Rate" from ball_by_ball,player where player."Player_Id"='+str(player_id)+' and player."Player_Id" = ball_by_ball."Bowler_Id" group by player."Player_Name",player."Player_Id" ')
    playername = cursor.fetchall()
    cursor2 = conn.cursor()
    cursor2.execute('SELECT player."Player_Name",player."Player_Id",sum("Batsman_Scored") as "Runs", CAST(sum("Batsman_Scored") as float)/CAST(count(*) as float) * 100 as "Strike Rate" from ball_by_ball,player where player."Player_Id"='+str(player_id)+' and player."Player_Id" = ball_by_ball."Striker_Id" group by player."Player_Name",player."Player_Id"')
    player_details1 = cursor2.fetchall()
    cursor3 = conn.cursor()
    cursor3.execute('SELECT  player."Player_Name",player."Player_Id",COUNT(*) as "Wickets" from ball_by_ball, player where  player."Player_Id"='+str(player_id)+' and player."Player_Id" = ball_by_ball."Bowler_Id" and ball_by_ball."Dismissal_Type" IN (\'caught\',\'lbw\',\'stumped\',\'bowled\',\'caught and bowled\') group by player."Player_Name",player."Player_Id"')
    player_details2 = cursor3.fetchall()
    bowlerStatistics = []
    for i in playername:
        x = {}
        x['Player_Name'] = i[0]
        x['Player_Id'] = int(i[1])
        x['Economy'] = float(i[2])
        bowlerStatistics.append(x)
    for j in player_details1:
        y = {}
        y['Runs'] = int(j[2])
        y['Player_Id'] = int(j[1])
        y['Strikerate'] = float(j[3])
        bowlerStatistics.append(y)
    for k in player_details2:
        z = {}
        z['Wickets'] = int(k[2])
        z['Player_Id'] = int(k[1])
        bowlerStatistics.append(z)
    cursor.close()
    cursor2.close()
    cursor3.close()
    conn.close()
    return json.dumps(bowlerStatistics)

##########################End of player endpoints##############################

########################### Season endpoints starts here############################
#####Author:KANNAN GANESAN




@app.route("/iplviz/season/teams/<id>")
def season_teams(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = id
    queryStr = 'SELECT "Season_Id" from season where "Season_Year"='+str(year)+''
    cursor.execute(queryStr)
    seasons=cursor.fetchall()
    for i in seasons:
        seasonid=int(i[0])
    cursor.execute('SELECT distinct "Team_Id","Team_Name" from (select distinct "Team_Id","Team_Name" from team,match where team."Team_Id"=match."Team_Name_Id" and match."Season_Id"='+str(seasonid)+' union select distinct "Team_Id","Team_Name" from team,match where team."Team_Id"=match."Opponent_Team_Id" and match."Season_Id"='+str(seasonid)+') as temp order by "Team_Id"')
    result=cursor.fetchall()
    teams=[]
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Season']=year
        x['Team_Name']=i[1]
        teams.append(x);
    cursor.close()
    conn.close()
    return json.dumps(teams)

#Done
@app.route("/iplviz/season/teamwins/<yr>")
def season_teamwins(yr):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = yr
    queryStr = 'SELECT "Season_Id" from season where "Season_Year"='+str(year)+''
    cursor.execute(queryStr)
    seasons=cursor.fetchall()
    for i in seasons:
        seasonid=int(i[0])
    cursor.execute('SELECT "Team_Id","Team_Name",count("Match_Winner_Id") from match,team where match."Season_Id"='+str(seasonid)+' and match."Match_Winner_Id"=team."Team_Id" group by "Team_Name","Team_Id"')
    result=cursor.fetchall()
    teamwins=[]
    for i in result:
        x={}
        x['Team_Id']=i[0]
        x['Team_Name']=i[1]
        x['Season_Year']=year
        x['Wins']=int(i[2])
        teamwins.append(x);
    cursor.close()
    conn.close()
    return json.dumps(teamwins)

#Done
@app.route("/iplviz/season/pointstable/<yr>")
def points_table(yr):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    year = yr
    queryStr = 'SELECT "Season_Id" from season where "Season_Year"='+str(year)+''
    cursor.execute(queryStr)
    seasons=cursor.fetchall()
    for i in seasons:
        seasonid=int(i[0])
    #cursor1 = conn.cursor()
    cursor.execute('SELECT "Team_Id",team."Team_Name",COUNT(match."Match_Winner_Id")*2 as Points,COUNT(match."Match_Winner_Id") as WON FROM match,team WHERE "Season_Id"='+str(seasonid)+' and team."Team_Id" = match."Match_Winner_Id" GROUP BY team."Team_Name","Team_Id"')
    cursor1.execute('select "Team_Name","Match_Winner_Id" from match,team where "Match_Winner_Id"=team."Team_Id" and "Match_Date"=(select max("Match_Date") from match where "Season_Id"='+str(seasonid)+')')
    result=cursor.fetchall()
    result1=cursor1.fetchall()
    winner=str(result1[0][0])
    print winner
    pointstable=[]
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Points']=int(i[2])
        x['Wins']=int(i[3])
        x['Team_Name']=i[1]
        x['Season_Year']=year
        if i[1]==winner:
            x['Season_Winner']='true'
        pointstable.append(x)
    cursor.close()
    conn.close()
    return json.dumps(pointstable)

#Done
@app.route("/iplviz/season/top3batsmen/<yr>")
def season_top3bat(yr):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = yr
    queryStr = 'SELECT "Season_Id" from season where "Season_Year"='+str(year)+''
    cursor.execute(queryStr)
    seasons=cursor.fetchall()
    for i in seasons:
        seasonid=int(i[0])
    cursor.execute('SELECT  "Player_Id",player."Player_Name",SUM("Batsman_Scored") from ball_by_ball, player where "Season_Id"='+str(seasonid)+' and player."Player_Id" = ball_by_ball."Striker_Id" group by "Player_Id",player."Player_Name" order by SUM("Batsman_Scored") DESC limit 3')
    result=cursor.fetchall()
    topbatsmen=[]
    for i in result:
        x={}
        x['Player_Id']=int(i[0])
        x['Player_Name']=i[1]
        x['Season_Year']=year
        x['Runs']=int(i[2])
        topbatsmen.append(x);
    cursor.close()
    conn.close()
    return json.dumps(topbatsmen)

#Done
@app.route("/iplviz/season/top3bowlers/<yr>")
def season_top3bowl(yr):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = yr
    queryStr = 'SELECT "Season_Id" from season where "Season_Year"='+str(year)+''
    cursor.execute(queryStr)
    seasons=cursor.fetchall()
    for i in seasons:
        seasonid=int(i[0])
    cursor.execute('SELECT "Player_Id",player."Player_Name",COUNT(ball_by_ball."Player_Dismissal_Id") from ball_by_ball, player where "Season_Id"='+str(seasonid)+'and player."Player_Id" = ball_by_ball."Bowler_Id" and ball_by_ball."Dismissal_Type" IN (\'caught\',\'lbw\',\'stumped\',\'bowled\',\'caught and bowled\') group by "Player_Id",player."Player_Name" order by count(ball_by_ball."Player_Dismissal_Id") DESC limit 3')
    result=cursor.fetchall()
    topbowlers=[]
    for i in result:
        x={}
        x['Player_Id']=int(i[0])
        x['Player_Name']=i[1]
        x['Season_Year']=year
        x['Wickets']=int(i[2])
        topbowlers.append(x);
    cursor.close()
    conn.close()
    return json.dumps(topbowlers)

#Done
@app.route("/iplviz/season/top3keepers/<yr>")
def season_top3keepers(yr):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = yr
    queryStr = 'SELECT "Season_Id" from season where "Season_Year"='+str(year)+''
    cursor.execute(queryStr)
    seasons=cursor.fetchall()
    for i in seasons:
        seasonid=int(i[0])
    cursor.execute('SELECT "Player_Id",player."Player_Name",COUNT(*) from ball_by_ball, player where ball_by_ball."Season_Id"='+str(seasonid)+' and player."Player_Id"= ball_by_ball."Fielder_Id" and ball_by_ball."Player_Dismissal_Id" not in (\' \') and ball_by_ball."Dismissal_Type" IN (\'caught\',\'stumped\') and player."Player_Id" in (SELECT match_player."player_id" from match_player where is_keeper=1) group by "Player_Id",player."Player_Name" order by count(ball_by_ball."Player_Dismissal_Id") DESC limit 3')
    result=cursor.fetchall()
    topkeepers=[]
    for i in result:
        x={}
        x['Player_Id']=int(i[0])
        x['Player_Name']=i[1]
        x['Season_Year']=year
        x['Dismissals']=int(i[2])
        topkeepers.append(x);
    cursor.close()
    conn.close()
    return json.dumps(topkeepers)


#Done
@app.route("/iplviz/season/top3partnership/<yr>")
def season_top3partners(yr):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = yr
    queryStr = 'SELECT "Season_Id" from season where "Season_Year"='+str(year)+''
    cursor.execute(queryStr)
    seasons=cursor.fetchall()
    for i in seasons:
        seasonid=int(i[0])
    cursor.execute('select temptable.A as C, temptable.B as D, sum(temptable.runs) as newruns from((select "Striker_Id" as A,"Non_Striker_Id" as B,sum("Batsman_Scored")+sum("Extra_Runs") as runs from ball_by_ball where "Season_Id"='+str(seasonid)+' group by "Striker_Id","Non_Striker_Id")union(select "Non_Striker_Id" as A,"Striker_Id" as B,sum("Batsman_Scored")+sum("Extra_Runs") as runs from ball_by_ball where "Season_Id"='+str(seasonid)+' group by "Non_Striker_Id","Striker_Id")) AS temptable where temptable.A < temptable.B group by C,D order by newruns desc limit 3')
    result=cursor.fetchall()
    toppartners=[]
    for i in result:
        x={}
        x['Player1_Id']=int(i[0])
        x['Season_Year']=year
        x['Player2_Id']=int(i[1])
        x['Runs']=int(i[2])
        toppartners.append(x);
    j=0
    y=[]
    z=[]
    while j < len(toppartners):
        y.append(toppartners[j]['Player1_Id'])
        z.append(toppartners[j]['Player2_Id'])
        j+=1

    player1=[]
    for id in y:
        cursor.execute('select "Player_Name" from player where "Player_Id"='+str(id)+'')
        result=cursor.fetchall()
        for i in result:
            player1.append(i[0])
    player2=[]
    for id in z:
        cursor.execute('select "Player_Name" from player where "Player_Id"='+str(id)+'')
        result=cursor.fetchall()
        for i in result:
            player2.append(i[0])
    finallist=[]
    loop=0
    while loop < len(player1):
        k={}
        k['Player1_Id']=toppartners[loop]['Player1_Id']
        k['Player2_Id']=toppartners[loop]['Player2_Id']
        k['Player1_Name']=player1[loop]
        k['Player2_Name']=player2[loop]
        k['Season']=toppartners[loop]['Season_Year']
        k['Runs']=toppartners[loop]['Runs']
        finallist.append(k)
        loop+=1
    print finallist
    cursor.close()
    conn.close()
    return json.dumps(finallist)

#Done
@app.route("/iplviz/season/teamrunrates/<yr>")
def season_teamrunrates(yr):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = yr
    queryStr = 'SELECT "Season_Id" from season where "Season_Year"='+str(year)+''
    cursor.execute(queryStr)
    seasons=cursor.fetchall()
    for i in seasons:
        seasonid=int(i[0])
    cursor.execute('SELECT "Team_Id","Team_Name",(CAST(sum("Batsman_Scored")+sum("Extra_Runs") as FLOAT)/CAST(count(*) as FLOAT))*6 as RUNRATE from ball_by_ball,team where "Season_Id"='+str(seasonid)+' and ball_by_ball."Team_Batting_Id"=team."Team_Id" group by "Team_Name","Team_Id"')
    result=cursor.fetchall()
    teamrunrates=[]
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Team_Name']=i[1]
        x['Season_Year']=year
        x['Run_Rate']=float(i[2])
        teamrunrates.append(x);
    cursor.execute('SELECT "Team_Id","Team_Name",(CAST(sum("Batsman_Scored")+sum("Extra_Runs") as FLOAT)/CAST(count(*) as FLOAT))*6 as RUNRATE from ball_by_ball,team where "Season_Id"='+str(seasonid)+' and ball_by_ball."Team_Bowling_Id"=team."Team_Id" group by "Team_Name","Team_Id"')
    result=cursor.fetchall()
    teameconomyrates=[]
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Team_Name']=i[1]
        x['Season_Year']=year
        x['Economy_Rate']=float(i[2])
        teameconomyrates.append(x);
    finallist=[]
    loop=0
    while loop < len(teameconomyrates):
        k={}
        k['Team_Id']=teamrunrates[loop]['Team_Id']
        k['Team_Name']=teamrunrates[loop]['Team_Name']
        k['Season_Year']=year
        k['Run_Rate']=teamrunrates[loop]['Run_Rate']
        k['Economy_Rate']=teameconomyrates[loop]['Economy_Rate']
        finallist.append(k)
        loop+=1
    cursor.close()
    conn.close()
    return json.dumps(finallist)


@app.route("/iplviz/season/teamslogruns/<yr>")
def season_teamslogruns(yr):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = 2008
    queryStr = 'SELECT "Season_Id" from season where "Season_Year"='+str(year)+''
    cursor.execute(queryStr)
    seasons=cursor.fetchall()
    for i in seasons:
        seasonid=int(i[0])
    cursor.execute('SELECT "Team_Id","Team_Name",sum("Batsman_Scored")+sum("Extra_Runs") from ball_by_ball,team where "Over_Id">=15 and "Over_Id"<=20 and "Season_Id"='+str(seasonid)+' and team."Team_Id"=ball_by_ball."Team_Batting_Id" group by "Team_Name","Team_Id" order by "Team_Name"')
    result=cursor.fetchall()
    teamslogruns=[]
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Team_Name']=i[1]
        x['Season_Year']=year
        x['Runs']=int(i[2])
        teamslogruns.append(x);
    teammiddleruns=[]
    cursor.execute('SELECT "Team_Id","Team_Name",sum("Batsman_Scored")+sum("Extra_Runs") from ball_by_ball,team where "Over_Id">=7 and "Over_Id"<=14 and "Season_Id"='+str(seasonid)+' and team."Team_Id"=ball_by_ball."Team_Batting_Id" group by "Team_Name","Team_Id" order by "Team_Name"')
    result=cursor.fetchall()
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Team_Name']=i[1]
        x['Season_Year']=year
        x['Runs']=int(i[2])
        teammiddleruns.append(x);
    teampowerruns=[]
    cursor.execute('SELECT "Team_Id","Team_Name",sum("Batsman_Scored")+sum("Extra_Runs") from ball_by_ball,team where "Over_Id">=1 and "Over_Id"<=6 and "Season_Id"='+str(seasonid)+' and team."Team_Id"=ball_by_ball."Team_Batting_Id" group by "Team_Name","Team_Id" order by "Team_Name"')
    result=cursor.fetchall()
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Team_Name']=i[1]
        x['Season_Year']=year
        x['Runs']=int(i[2])
        teampowerruns.append(x);
    loop=0
    finallist=[]
    while loop < len(teampowerruns):
        k={}
        k['Team_Id']=teampowerruns[loop]['Team_Id']
        k['Team_Name']=teampowerruns[loop]['Team_Name']
        k['Season_Year']=year
        k['Powerruns']=teampowerruns[loop]['Runs']
        k['Middleruns']=teammiddleruns[loop]['Runs']
        k['Slogruns']=teamslogruns[loop]['Runs']
        finallist.append(k)
        loop+=1
    cursor.close()
    conn.close()
    return json.dumps(finallist)

@app.route("/iplviz/season/teamboundruns/<yr>")
def season_teamboundruns(yr):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = yr
    queryStr = 'SELECT "Season_Id" from season where "Season_Year"='+str(year)+''
    cursor.execute(queryStr)
    seasons=cursor.fetchall()
    for i in seasons:
        seasonid=int(i[0])
    cursor.execute('SELECT "Team_Id","Team_Name",sum("Batsman_Scored")+sum("Extra_Runs") from ball_by_ball,team where "Season_Id"='+str(seasonid)+' and ("Batsman_Scored" not in(4,6) or "Extra_Runs" not in(4,6)) and ball_by_ball."Team_Batting_Id"=team."Team_Id" group by "Team_Name","Team_Id"')
    result=cursor.fetchall()
    totalruns=[]
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Team_Name']=i[1]
        x['Season_Year']=year
        x['Runs']=int(i[2])
        totalruns.append(x);
    cursor.execute('select "Team_Id","Team_Name",sum("Batsman_Scored")+sum("Extra_Runs") from ball_by_ball,team where "Season_Id"='+str(seasonid)+'  and ("Batsman_Scored" in(4,6) or "Extra_Runs" in(4,6)) and ball_by_ball."Team_Batting_Id"=team."Team_Id" group by "Team_Name","Team_Id"')
    result=cursor.fetchall()
    boundruns=[]
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Team_Name']=i[1]
        x['Season_Year']=year
        x['Runs']=int(i[2])
        boundruns.append(x);
    finallist=[]
    loop=0
    while loop < len(boundruns):
        k={}
        k['Team_Id']=totalruns[loop]['Team_Id']
        k['Team_Name']=totalruns[loop]['Team_Name']
        k['Season']=year
        k['Total_Runs']=totalruns[loop]['Runs']-boundruns[loop]['Runs']
        k['Bound_Runs']=boundruns[loop]['Runs']
        finallist.append(k)
        loop+=1
    print finallist
    cursor.close()
    conn.close()
    return json.dumps(finallist)

@app.route("/iplviz/season/teamslogrunrates/<yr>")
def season_teamslogrunrates(yr):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = yr
    queryStr = 'SELECT "Season_Id" from season where "Season_Year"='+str(year)+''
    cursor.execute(queryStr)
    seasons=cursor.fetchall()
    for i in seasons:
        seasonid=int(i[0])
    cursor.execute('SELECT "Team_Id","Team_Name",(CAST(sum("Batsman_Scored")+sum("Extra_Runs") as FLOAT)/CAST(count(*) as FLOAT))*6 as RUNRATE from ball_by_ball,team where "Season_Id"='+str(seasonid)+' and team."Team_Id"=ball_by_ball."Team_Batting_Id" and "Over_Id">=15 and "Over_Id"<=20 group by "Team_Name","Team_Id"')
    result=cursor.fetchall()
    teamslogrunrates=[]
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Team_Name']=i[1]
        x['Season_Year']=year
        x['Run_Rate']=float(i[2])
        teamslogrunrates.append(x);
    cursor.execute('SELECT "Team_Id","Team_Name",(CAST(sum("Batsman_Scored")+sum("Extra_Runs") as FLOAT)/CAST(count(*) as FLOAT))*6 as ECONOMY from ball_by_ball,team where "Season_Id"='+str(seasonid)+' and team."Team_Id"=ball_by_ball."Team_Bowling_Id" and "Over_Id">=15 and "Over_Id"<=20 group by "Team_Name","Team_Id"')
    result=cursor.fetchall()
    teamslogeconrates=[]
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Team_Name']=i[1]
        x['Season_Year']=year
        x['Econ_Rate']=float(i[2])
        teamslogeconrates.append(x);
    loop=0
    finallist=[]
    while loop < len(teamslogeconrates):
        k={}
        k['Team_Id']=teamslogrunrates[loop]['Team_Id']
        k['Team_Name']=teamslogrunrates[loop]['Team_Name']
        k['Season_Year']=year
        k['Run_Rate']=teamslogrunrates[loop]['Run_Rate']
        k['Economy_Rate']=teamslogeconrates[loop]['Econ_Rate']
        finallist.append(k)
        loop+=1
    cursor.close()
    conn.close()
    return json.dumps(finallist)


##################################################Season endpoints ends here#############################################


##############################################Match endpoints starts here####################################
#Done
@app.route("/iplviz/match/<id>")
def match_data(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    cursor3 = conn.cursor()
    matchid=id
    cursor.execute('SELECT "Over_Id",sum("Batsman_Scored")+sum("Extra_Runs") as "Total_Runs" from "ball_by_ball" where "Match_Id"='+str(matchid)+' and "Innings_Id"=2 group by "Over_Id" limit 100;')
    cursor1.execute('SELECT "Over_Id",sum("Batsman_Scored")+sum("Extra_Runs") as "Total_Runs" from "ball_by_ball" where "Match_Id"='+str(matchid)+' and "Innings_Id"=1 group by "Over_Id" limit 100')
    cursor2.execute('select distinct team."Team_Name" from ball_by_ball,team where ball_by_ball."Match_Id"='+str(matchid)+' and "Innings_Id"=1 and ball_by_ball."Team_Batting_Id"=team."Team_Id"')
    cursor3.execute('select distinct team."Team_Name" from ball_by_ball,team where ball_by_ball."Match_Id"='+str(matchid)+' and "Innings_Id"=2 and ball_by_ball."Team_Batting_Id"=team."Team_Id"')
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

#Done
@app.route("/iplviz/match/t1topbatsmen/<id>")
def match_t1top3bat(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    matchid=id
    cursor.execute('SELECT "Player_Id","Player_Name" as A,sum("Batsman_Scored") as "Total_Runs" from "ball_by_ball","player"  WHERE "Team_Batting_Id"=(select "Team_Name_Id" from match where "Match_Id"='+str(matchid)+') and "Match_Id"='+str(matchid)+' and "Striker_Id" = "Player_Id" group by "Player_Name","Player_Id" order by "Total_Runs" desc limit 3')
    result=cursor.fetchall()
    topbatsmen=[]
    for i in result:
        x={}
        x['Player_Id']=int(i[0])
        x['Player_Name']=i[1]
        x['Runs']=int(i[2])
        topbatsmen.append(x);
    cursor.close()
    conn.close()
    return json.dumps(topbatsmen)

#Done
@app.route("/iplviz/match/t2topbatsmen/<id>")
def match_t2top3bat(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    matchid=id
    cursor.execute('SELECT "Player_Id","Player_Name" as A,sum("Batsman_Scored") as "Total_Runs" from "ball_by_ball","player"  WHERE "Team_Batting_Id"=(select "Opponent_Team_Id" from match where "Match_Id"='+str(matchid)+') and "Match_Id"='+str(matchid)+' and "Striker_Id" = "Player_Id" group by "Player_Name","Player_Id" order by "Total_Runs" desc limit 3')
    result=cursor.fetchall()
    topbatsmen=[]
    for i in result:
        x={}
        x['Player_Id']=int(i[0])
        x['Player_Name']=i[1]
        x['Runs']=int(i[2])
        topbatsmen.append(x);
    cursor.close()
    conn.close()
    return json.dumps(topbatsmen)

#Done
@app.route("/iplviz/match/t1topbowlers/<id>")
def match_t1topbowlers(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    matchid=id
    cursor.execute('SELECT "Player_Name","Bowler_Id", count(*) as "Total_Wickets" from ball_by_ball,player where "Team_Bowling_Id" in (select "Team_Name_Id" from match where "Match_Id"='+str(matchid)+') and "Match_Id" ='+str(matchid)+' and ball_by_Ball."Bowler_Id"=player."Player_Id" and "Dismissal_Type" not in (\' \',\'retired hurt\',\'run out\') group by "Bowler_Id","Player_Name" order by "Total_Wickets" desc limit 3')
    result=cursor.fetchall()
    topbowlers=[]
    for i in result:
        x={}
        x['Player_Id']=int(i[1])
        x['Player_Name']=i[0]
        x['Wickets']=int(i[2])
        topbowlers.append(x);
    print(topbowlers)
    j=0
    y=[]
    while j < len(topbowlers):
        y.append(topbowlers[j]['Player_Id'])
        j+=1

    runsgiven=[]
    for id in y:
        cursor.execute('select "Player_Name","Bowler_Id", sum("Batsman_Scored")+sum("Extra_Runs") as "Total_Runs" from ball_by_ball,player where "Match_Id" = '+str(matchid)+' and ball_by_Ball."Bowler_Id"=player."Player_Id" and "Bowler_Id"='+str(id)+' group by "Bowler_Id","Player_Name" order by "Total_Runs" desc limit 3')
        result=cursor.fetchall()
        for i in result:
            runsgiven.append(int(i[2]))
    finallist=[]
    loop=0
    while loop < len(runsgiven):
        k={}
        k['Player_Id']=topbowlers[loop]['Player_Id']
        k['Player1_Name']=topbowlers[loop]['Player_Name']
        k['Wickets']=topbowlers[loop]['Wickets']
        k['Runs']=runsgiven[loop]
        finallist.append(k)
        loop+=1
    cursor.close()
    conn.close()
    return json.dumps(finallist)

#Done
@app.route("/iplviz/match/t2topbowlers/<id>")
def match_t2topbowlers(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    matchid=id
    cursor.execute('SELECT "Player_Name","Bowler_Id", count(*) as "Total_Wickets" from ball_by_ball,player where "Team_Bowling_Id" in (select "Opponent_Team_Id" from match where "Match_Id"='+str(matchid)+') and "Match_Id" ='+str(matchid)+' and ball_by_Ball."Bowler_Id"=player."Player_Id" and "Dismissal_Type" not in (\' \',\'retired hurt\',\'run out\') group by "Bowler_Id","Player_Name" order by "Total_Wickets" desc limit 3')
    result=cursor.fetchall()
    topbowlers=[]
    for i in result:
        x={}
        x['Player_Id']=int(i[1])
        x['Player_Name']=i[0]
        x['Wickets']=int(i[2])
        topbowlers.append(x);
    print(topbowlers)
    j=0
    y=[]
    while j < len(topbowlers):
        y.append(topbowlers[j]['Player_Id'])
        j+=1

    runsgiven=[]
    for id in y:
        cursor.execute('select "Player_Name","Bowler_Id", sum("Batsman_Scored")+sum("Extra_Runs") as "Total_Runs" from ball_by_ball,player where "Match_Id" = '+str(matchid)+' and ball_by_Ball."Bowler_Id"=player."Player_Id" and "Bowler_Id"='+str(id)+' group by "Bowler_Id","Player_Name" order by "Total_Runs" desc limit 3')
        result=cursor.fetchall()
        for i in result:
            runsgiven.append(int(i[2]))
    finallist=[]
    loop=0
    while loop < len(runsgiven):
        k={}
        k['Player_Id']=topbowlers[loop]['Player_Id']
        k['Player1_Name']=topbowlers[loop]['Player_Name']
        k['Wickets']=topbowlers[loop]['Wickets']
        k['Runs']=runsgiven[loop]
        finallist.append(k)
        loop+=1
    cursor.close()
    conn.close()
    return json.dumps(finallist)

#Done
@app.route("/iplviz/match/teamruns")
def match_teamruns():
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    matchid=335988
    cursor.execute('select "Team_Batting_Id","Team_Name","Over_Id",sum("Batsman_Scored")+sum("Extra_Runs") as "Total_Runs" from "ball_by_ball",team where "Match_Id"='+str(matchid)+' and ("Team_Batting_Id" = (select "Team_Name_Id" from match where "Match_Id"='+str(matchid)+') or "Team_Batting_Id" = (select "Opponent_Team_Id" from match where "Match_Id"='+str(matchid)+')) and "Team_Batting_Id"="Team_Id" group by "Over_Id","Team_Batting_Id","Team_Name" order by "Over_Id" asc')
    result=cursor.fetchall()
    teamruns=[]
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Team_Name']=i[1]
        x['Over_Id']=int(i[2])
        x['Runs']=int(i[3])
        teamruns.append(x);
    cursor.close()
    conn.close()
    return json.dumps(teamruns)

#Done
@app.route("/iplviz/match/t1top3partnership/<id>")
def match_t1top3partners(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    matchid=id
    cursor.execute('select temptable.A as C, temptable.B as D, sum(temptable.runs) as newruns from((select "Striker_Id" as A,"Non_Striker_Id" as B,sum("Batsman_Scored")+sum("Extra_Runs") as runs from ball_by_ball where "Season_Id"=1 and "Match_Id"='+str(matchid)+'  and "Team_Batting_Id" = (select DISTINCT "Team_Name_Id" from match where "Match_Id" = '+str(matchid)+') group by "Striker_Id","Non_Striker_Id")union  (select "Non_Striker_Id" as A,"Striker_Id" as B,sum("Batsman_Scored")+sum("Extra_Runs") as runs from ball_by_ball where "Season_Id"=1 and "Match_Id"='+str(matchid)+' and "Team_Batting_Id" = (select DISTINCT "Team_Name_Id" from match where "Match_Id" = '+str(matchid)+') group by "Non_Striker_Id","Striker_Id")) AS temptable where temptable.A < temptable.B group by C,D order by newruns desc limit 3;')
    result=cursor.fetchall()
    toppartners=[]
    for i in result:
        x={}
        x['Player1_Id']=int(i[0])
        x['Player2_Id']=int(i[1])
        x['Runs']=int(i[2])
        toppartners.append(x);
    j=0
    y=[]
    z=[]
    while j < len(toppartners):
        y.append(toppartners[j]['Player1_Id'])
        z.append(toppartners[j]['Player2_Id'])
        j+=1

    player1=[]
    for id in y:
        cursor.execute('select "Player_Name" from player where "Player_Id"='+str(id)+'')
        result=cursor.fetchall()
        for i in result:
            player1.append(i[0])
    player2=[]
    for id in z:
        cursor.execute('select "Player_Name" from player where "Player_Id"='+str(id)+'')
        result=cursor.fetchall()
        for i in result:
            player2.append(i[0])
    finallist=[]
    loop=0
    while loop < len(player1):
        k={}
        k['Player1_Id']=toppartners[loop]['Player1_Id']
        k['Player2_Id']=toppartners[loop]['Player2_Id']
        k['Player1_Name']=player1[loop]
        k['Player2_Name']=player2[loop]
        k['Runs']=toppartners[loop]['Runs']
        finallist.append(k)
        loop+=1
    cursor.close()
    conn.close()
    return json.dumps(finallist)


#Done
@app.route("/iplviz/match/t2top3partnership/<id>")
def match_t2top3partners(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    matchid=id
    cursor.execute('select temptable.A as C, temptable.B as D, sum(temptable.runs) as newruns from((select "Striker_Id" as A,"Non_Striker_Id" as B,sum("Batsman_Scored")+sum("Extra_Runs") as runs from ball_by_ball where "Season_Id"=1 and "Match_Id"='+str(matchid)+'  and "Team_Batting_Id" = (select DISTINCT "Opponent_Team_Id" from match where "Match_Id" = '+str(matchid)+') group by "Striker_Id","Non_Striker_Id")union  (select "Non_Striker_Id" as A,"Striker_Id" as B,sum("Batsman_Scored")+sum("Extra_Runs") as runs from ball_by_ball where "Season_Id"=1 and "Match_Id"='+str(matchid)+' and "Team_Batting_Id" = (select DISTINCT "Opponent_Team_Id" from match where "Match_Id" = '+str(matchid)+') group by "Non_Striker_Id","Striker_Id")) AS temptable where temptable.A < temptable.B group by C,D order by newruns desc limit 3;')
    result=cursor.fetchall()
    toppartners=[]
    for i in result:
        x={}
        x['Player1_Id']=int(i[0])
        x['Player2_Id']=int(i[1])
        x['Runs']=int(i[2])
        toppartners.append(x);
    j=0
    y=[]
    z=[]
    while j < len(toppartners):
        y.append(toppartners[j]['Player1_Id'])
        z.append(toppartners[j]['Player2_Id'])
        j+=1

    player1=[]
    for id in y:
        cursor.execute('select "Player_Name" from player where "Player_Id"='+str(id)+'')
        result=cursor.fetchall()
        for i in result:
            player1.append(i[0])
    player2=[]
    for id in z:
        cursor.execute('select "Player_Name" from player where "Player_Id"='+str(id)+'')
        result=cursor.fetchall()
        for i in result:
            player2.append(i[0])
    finallist=[]
    loop=0
    while loop < len(player1):
        k={}
        k['Player1_Id']=toppartners[loop]['Player1_Id']
        k['Player2_Id']=toppartners[loop]['Player2_Id']
        k['Player1_Name']=player1[loop]
        k['Player2_Name']=player2[loop]
        k['Runs']=toppartners[loop]['Runs']
        finallist.append(k)
        loop+=1
    cursor.close()
    conn.close()
    return json.dumps(finallist)

#Done
@app.route("/iplviz/match/team1powerruns/<id>")
def match_team1powerruns(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    matchid=id
    cursor.execute('select "Team_Batting_Id","Team_Name",sum("Batsman_Scored")+sum("Extra_Runs") as "Runs_In_Powerplay" from ball_by_ball,team where "Match_Id" = '+str(matchid)+' and "Over_Id" >= 1 and "Over_Id" <=6 and "Team_Batting_Id" in (select "Team_Name_Id" from match where "Match_Id" = '+str(matchid)+') and team."Team_Id"="Team_Batting_Id" group by "Team_Batting_Id","Team_Name"')
    result=cursor.fetchall()
    teamruns=[]
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Team_Name']=i[1]
        x['Runs']=int(i[2])
        teamruns.append(x);
    if not teamruns:
        j={}
        j['Runs']=0
        teamruns.append(j);
    cursor.execute('select "Team_Batting_Id","Team_Name",sum("Batsman_Scored")+sum("Extra_Runs") as "Runs_In_Powerplay" from ball_by_ball,team where "Match_Id" = '+str(matchid)+' and "Over_Id" >= 7 and "Over_Id" <=14 and "Team_Batting_Id" in (select "Team_Name_Id" from match where "Match_Id" = '+str(matchid)+') and team."Team_Id"="Team_Batting_Id" group by "Team_Batting_Id","Team_Name"')
    result=cursor.fetchall()
    teammiddleruns=[]
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Team_Name']=i[1]
        x['Runs']=int(i[2])
        teammiddleruns.append(x);
    if not teammiddleruns:
        j={}
        j['Runs']=0
        teammiddleruns.append(j);
    cursor.execute('select "Team_Batting_Id","Team_Name",sum("Batsman_Scored")+sum("Extra_Runs") as "Runs_In_Powerplay" from ball_by_ball,team where "Match_Id" = '+str(matchid)+' and "Over_Id" >= 15 and "Over_Id" <=20 and "Team_Batting_Id" in (select "Team_Name_Id" from match where "Match_Id" = '+str(matchid)+') and team."Team_Id"="Team_Batting_Id" group by "Team_Batting_Id","Team_Name"')
    result=cursor.fetchall()
    teamslogruns=[]
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Team_Name']=i[1]
        x['Runs']=int(i[2])
        teamslogruns.append(x);
    if not teamslogruns:
        j={}
        j['Runs']=0
        teamslogruns.append(j);
    loop=0
    finallist=[]
    while loop < len(teamslogruns):
        k={}
        k['Team_Id']=teamruns[loop]['Team_Id']
        k['Team_Name']=teamruns[loop]['Team_Name']
        k['Powerruns']=teamruns[loop]['Runs']
        k['Middleruns']=teammiddleruns[loop]['Runs']
        k['Slogruns']=teamslogruns[loop]['Runs']
        finallist.append(k)
        loop+=1
    cursor.close()
    conn.close()
    return json.dumps(finallist)

#Done
@app.route("/iplviz/match/team2powerruns/<id>")
def match_team2powerruns(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    matchid=id
    cursor.execute('select "Team_Batting_Id","Team_Name",sum("Batsman_Scored")+sum("Extra_Runs") as "Runs_In_Powerplay" from ball_by_ball,team where "Match_Id" = '+str(matchid)+' and "Over_Id" >= 1 and "Over_Id" <=6 and "Team_Batting_Id" in (select "Opponent_Team_Id" from match where "Match_Id" = '+str(matchid)+') and team."Team_Id"="Team_Batting_Id" group by "Team_Batting_Id","Team_Name"')
    result=cursor.fetchall()
    teamruns=[]
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Team_Name']=i[1]
        x['Runs']=int(i[2])
        teamruns.append(x);
    if not teamruns:
        j={}
        j['Runs']=0
        teamruns.append(j);
    cursor.execute('select "Team_Batting_Id","Team_Name",sum("Batsman_Scored")+sum("Extra_Runs") as "Runs_In_Powerplay" from ball_by_ball,team where "Match_Id" = '+str(matchid)+' and "Over_Id" >= 7 and "Over_Id" <=14 and "Team_Batting_Id" in (select "Opponent_Team_Id" from match where "Match_Id" = '+str(matchid)+') and team."Team_Id"="Team_Batting_Id" group by "Team_Batting_Id","Team_Name"')
    result=cursor.fetchall()
    teammiddleruns=[]
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Team_Name']=i[1]
        x['Runs']=int(i[2])
        teammiddleruns.append(x);
    if not teammiddleruns:
        j={}
        j['Runs']=0
        teammiddleruns.append(j);
    cursor.execute('select "Team_Batting_Id","Team_Name",sum("Batsman_Scored")+sum("Extra_Runs") as "Runs_In_Powerplay" from ball_by_ball,team where "Match_Id" = '+str(matchid)+' and "Over_Id" >= 15 and "Over_Id" <=20 and "Team_Batting_Id" in (select "Opponent_Team_Id" from match where "Match_Id" = '+str(matchid)+') and team."Team_Id"="Team_Batting_Id" group by "Team_Batting_Id","Team_Name"')
    result=cursor.fetchall()
    teamslogruns=[]
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Team_Name']=i[1]
        x['Runs']=int(i[2])
        teamslogruns.append(x);
    if not teamslogruns:
        j={}
        j['Runs']=0
        teamslogruns.append(j);
    loop=0
    finallist=[]
    while loop < len(teamslogruns):
        k={}
        k['Team_Id']=teamruns[loop]['Team_Id']
        k['Team_Name']=teamruns[loop]['Team_Name']
        k['Powerruns']=teamruns[loop]['Runs']
        k['Middleruns']=teammiddleruns[loop]['Runs']
        k['Slogruns']=teamslogruns[loop]['Runs']
        finallist.append(k)
        loop+=1
    cursor.close()
    conn.close()
    return json.dumps(finallist)



@app.route("/iplviz/match/team1powerwickets/<id>")
def match_teampowerwickets(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    matchid=id
    cursor.execute('select "Team_Name","Team_Name_Id" from match,team where match."Team_Name_Id"=team."Team_Id" and "Match_Id"='+str(matchid))
    result=cursor.fetchall()
    teams=[]
    for i in result:
        x={}
        x['Team_Id']=i[0]
        x['Team_Name']=int(i[1])
        teams.append(x);
    cursor.execute('select "Team_Bowling_Id","Team_Name",count(*) as "Wicktes_In_Powerplay" from ball_by_ball,team where "Match_Id" = '+str(matchid)+' and "Over_Id" >= 1 and "Over_Id" <=6 and "Dismissal_Type" not in (\' \',\'retired hurt\') and "Team_Bowling_Id" in (select "Team_Name_Id" from match where "Match_Id" = '+str(matchid)+') and "Team_Id"="Team_Bowling_Id" group by "Team_Bowling_Id","Team_Name"')
    result=cursor.fetchall()
    print('Powerplay',result)
    teampower=[]
    for i in result:
        x={}
        x['Wickets']=int(i[2])
        teampower.append(x);
    if not teampower:
        j={}
        j['Wickets']=0
        teampower.append(j);

    cursor.execute('select "Team_Bowling_Id","Team_Name",count(*) as "Wicktes_In_Powerplay" from ball_by_ball,team where "Match_Id" = '+str(matchid)+' and "Over_Id" >= 7 and "Over_Id" <=14 and "Dismissal_Type" not in (\' \',\'retired hurt\') and "Team_Bowling_Id" in (select "Team_Name_Id" from match where "Match_Id" = '+str(matchid)+') and "Team_Id"="Team_Bowling_Id" group by "Team_Bowling_Id","Team_Name"')
    result=cursor.fetchall()
    print('middle',result)
    teammiddle=[]
    for i in result:
        print('for team middle')
        x={}
        x['Wickets']=int(i[2])
        teammiddle.append(x);
    if not teammiddle:
        print('if case middle')
        j={}
        j['Wickets']=0
        teammiddle.append(j);
    print('MiddleArray',teammiddle)
    cursor.execute('select "Team_Bowling_Id","Team_Name",count(*) as "Wicktes_In_Powerplay" from ball_by_ball,team where "Match_Id" = '+str(matchid)+' and "Over_Id" >= 15 and "Over_Id" <=20 and "Dismissal_Type" not in (\' \',\'retired hurt\') and "Team_Bowling_Id" in (select "Team_Name_Id" from match where "Match_Id" = '+str(matchid)+') and "Team_Id"="Team_Bowling_Id" group by "Team_Bowling_Id","Team_Name"')
    result=cursor.fetchall()
    print('slog',result)
    teamslog=[]
    for i in result:
        x={}
        x['Wickets']=int(i[2])
        teamslog.append(x);
    if not teamslog:
        j={}
        j['Wickets']=0
        teamslog.append(j);
    loop=0
    finallist=[]
    print()
    while loop < len(teamslog):
        k={}
        k['Team_Id']=teams[loop]['Team_Id']
        k['Team_Name']=teams[loop]['Team_Name']
        k['Power']=teampower[loop]['Wickets']
        k['Middle']=teammiddle[loop]['Wickets']
        k['Slog']=teamslog[loop]['Wickets']
        finallist.append(k)
        loop+=1
    cursor.close()
    conn.close()
    return json.dumps(finallist)


@app.route("/iplviz/match/team2powerwickets/<id>")
def match_team2powerwickets(id):
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    matchid=id
    cursor.execute('select "Team_Name","Team_Name_Id" from match,team where match."Team_Name_Id"=team."Team_Id" and "Match_Id"='+str(matchid))
    result=cursor.fetchall()
    teams=[]
    for i in result:
        x={}
        x['Team_Id']=i[0]
        x['Team_Name']=int(i[1])
        teams.append(x);
    cursor.execute('select "Team_Bowling_Id","Team_Name",count(*) as "Wicktes_In_Powerplay" from ball_by_ball,team where "Match_Id" = '+str(matchid)+' and "Over_Id" >= 1 and "Over_Id" <=6 and "Dismissal_Type" not in (\' \',\'retired hurt\') and "Team_Bowling_Id" in (select "Opponent_Team_Id" from match where "Match_Id" = '+str(matchid)+') and "Team_Id"="Team_Bowling_Id" group by "Team_Bowling_Id","Team_Name"')
    result=cursor.fetchall()
    print('Powerplay',result)
    teampower=[]
    for i in result:
        x={}
        x['Wickets']=int(i[2])
        teampower.append(x);
    if not teampower:
        j={}
        j['Wickets']=0
        teampower.append(j);

    cursor.execute('select "Team_Bowling_Id","Team_Name",count(*) as "Wicktes_In_Powerplay" from ball_by_ball,team where "Match_Id" = '+str(matchid)+' and "Over_Id" >= 7 and "Over_Id" <=14 and "Dismissal_Type" not in (\' \',\'retired hurt\') and "Team_Bowling_Id" in (select "Opponent_Team_Id" from match where "Match_Id" = '+str(matchid)+') and "Team_Id"="Team_Bowling_Id" group by "Team_Bowling_Id","Team_Name"')
    result=cursor.fetchall()
    print('middle',result)
    teammiddle=[]
    for i in result:
        print('for team middle')
        x={}
        x['Wickets']=int(i[2])
        teammiddle.append(x);
    if not teammiddle:
        print('if case middle')
        j={}
        j['Wickets']=0
        teammiddle.append(j);
    print('MiddleArray',teammiddle)
    cursor.execute('select "Team_Bowling_Id","Team_Name",count(*) as "Wicktes_In_Powerplay" from ball_by_ball,team where "Match_Id" = '+str(matchid)+' and "Over_Id" >= 15 and "Over_Id" <=20 and "Dismissal_Type" not in (\' \',\'retired hurt\') and "Team_Bowling_Id" in (select "Opponent_Team_Id" from match where "Match_Id" = '+str(matchid)+') and "Team_Id"="Team_Bowling_Id" group by "Team_Bowling_Id","Team_Name"')
    result=cursor.fetchall()
    print('slog',result)
    teamslog=[]
    for i in result:
        x={}
        x['Wickets']=int(i[2])
        teamslog.append(x);
    if not teamslog:
        j={}
        j['Wickets']=0
        teamslog.append(j);
    loop=0
    finallist=[]
    print()
    while loop < len(teamslog):
        k={}
        k['Team_Id']=teams[loop]['Team_Id']
        k['Team_Name']=teams[loop]['Team_Name']
        k['Power']=teampower[loop]['Wickets']
        k['Middle']=teammiddle[loop]['Wickets']
        k['Slog']=teamslog[loop]['Wickets']
        finallist.append(k)
        loop+=1
    cursor.close()
    conn.close()
    return json.dumps(finallist)


###########################################End of matchendpoints#############################################################################3

#############################################Team endpoints starts here################################
###################Author:Anjali##################

###################################### TEAM VISUALIZATION #############################################################
###################### AUTHOR - ANJALI
@app.route("/iplviz/team/<id>/<yr>")   #initial load
def team_getPlayersName(id,yr):
    #conn_string = "host='localhost' dbname='ipldata-dv' user='postgres' password='piyush'"
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    #teamName = "Kolkata Knight Riders"
    #cursor.execute('SELECT "Team_Id" from team where "Team_Name"=%s',(teamName,))
    #team = cursor.fetchone()
    teamId = id
    year = yr
    cursor.execute('select "Season_Id" from season where "Season_Year"='+str(year))
    season = cursor.fetchone()
    #seasonId = season[0]
    seasonId=season[0]
    cursor.execute('select "Player_Name","Player_Id" from player where "Player_Id" in (select DISTINCT "player_id" from "match_player" where "team_id" = %s and "Season_Id" = %s)',(str(teamId),str(seasonId)))
    result = cursor.fetchall()
    teamruns=[]
   # list2 = {}
   # list2 = {"Players": [{'Player Name': key, 'Player_Id': value} for key, value in result]}
    for i in result:
        x={}
        x['Player_Id']=int(i[1])
        x['Player_Name']=i[0]
        teamruns.append(x);
    #records = json.dumps(list2, indent=4)
    conn.close()
    return json.dumps(teamruns)



@app.route("/iplviz/team/winsfordifferentcity/<id>/<yr>")   #not wrt season because data is not enough for map
def team_getwinsfordifferentcity(id,yr):
    #conn_string = "host='localhost' dbname='ipldata-dv' user='postgres' password='piyush'"
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    teamId = id
    cursor.execute('SELECT "City_Name",count(*) from "match" WHERE "Match_Winner_Id"='+str(teamId)+' group by "City_Name"')
    result = cursor.fetchall()
    #list2 = {}
    #list2 = {"Number of Wins for different city": [{'City': key, 'Number Of Wins': value} for key, value in result]}
    #records = json.dumps(list2, indent=4)
    teamwins=[]
    for i in result:
        x={}
        x['City']=i[0]
        x['Wins']=int(i[1])
        teamwins.append(x);
    conn.close()
    return json.dumps(teamwins)



################ Line chart showing positions of team over the years(Winner,Runner,Eliminator,Qualifier,League stage)

@app.route("/iplviz/team/positionofteam/<id>")
def team_getPositionOfTeam(id):
    #conn_string = "host='localhost' dbname='ipldata-dv' user='postgres' password='piyush'"
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    teamName = "Kolkata Knight Riders"
    cursor.execute('SELECT "Team_Id" from team where "Team_Name"=%s', (teamName,))
    team = cursor.fetchone()
    teamId = team[0]
    list2 = []
    positionList = []
    for i in range(1,10):
        cursor.execute('select "match"."Team_Name_Id","match"."Opponent_Team_Id","match"."Match_Winner_Id" from "match" where "match"."Season_Id" = %s order by "match"."Match_Date" desc limit 4;',(str(i),))
        result = cursor.fetchall()
    #list2 = {"Position Of Team": [{'Team_Name_Id': row[0], 'Opponent_Team_Id': row[1], 'Match_Winner_Id':row[2]} for row in result]}
        count = 1
        position = "League"
        for row in result:
            if row[2] == teamId and count==1:
                position = "Winner"
                break;
            elif (row[0] == teamId or row[1] == teamId) and count == 1:
                position = "Runner"
                break;
            elif count==2 and (row[0]==teamId or row[1]==teamId or row[2]==teamId):
                position = "Qualifier"
                break;
            elif count == 3 and (row[0] == teamId or row[1] == teamId or row[2] == teamId):
                position = "Eliminator"
                break;
            elif count==4 and (row[0]==teamId or row[1]==teamId or row[2]==teamId):
                position =  "Qualifier"
                break;
            count = count+1

        cursor.execute('select "Season_Year" from season where "Season_Id"=%s', (str(i),))
        season = cursor.fetchone()
        year = season[0]
        positionList.append({'Season_Year': year,'Team_Name':teamName,'Pos':position})
    list2=positionList
    records = json.dumps(list2, indent=4)
    conn.close()
    return records

################## Line chart showing the run rate(scored and conceded) of team in different seasons

#Done
@app.route("/iplviz/team/scoreandconceded/<id>/<yr>")
def team_getTeamScoreandConceded(id,yr):
    #conn_string = "host='localhost' dbname='ipldata-dv' user='postgres' password='piyush'"
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    teamId = id
    year = yr
    cursor.execute('select "Season_Id" from season where "Season_Year"=%s', (str(year),))
    season = cursor.fetchone()
    seasonId = season[0]
    cursor.execute('select count(*) from "match" where "Season_Id" = %s and ("Team_Name_Id" = %s or "Opponent_Team_Id" =%s) ',(str(seasonId),str(teamId),str(teamId)))
    result= cursor.fetchone()
    cursor1.execute('select sum("Batsman_Scored")+sum("Extra_Runs") as "Total_Runs" from "ball_by_ball","match" where "match"."Match_Id" = "ball_by_ball"."Match_Id" and "Team_Batting_Id" = %s and "match"."Season_Id"=%s;',(str(teamId),str(seasonId)))
    cursor2.execute('select sum("Batsman_Scored")+sum("Extra_Runs") as "Total_Runs" from "ball_by_ball","match" where "match"."Match_Id" = "ball_by_ball"."Match_Id" and "Team_Bowling_Id" = %s and "match"."Season_Id"=%s;',(str(teamId),str(seasonId)))
    result1 = cursor1.fetchone()
    result2 =  cursor2.fetchone()
    numberOfOvers = 20.0
    numberOfMatches = result[0]
    numberOfRunsScored = result1[0]
    numberOfRunsConceded = result2[0]
    mul = 0
    mul = numberOfMatches * numberOfOvers
    ScoredRun = 0
    ScoredRun = float("{0:.2f}".format(numberOfRunsScored/mul));
    list2 = {}
    ConcededRun = float("{0:.2f}".format(numberOfRunsConceded/mul));
    scores={}
    scores['RunRate']=ScoredRun
    scores['Economy_Rate']=ConcededRun
    finallist=[]
    finallist.append(scores)
    #list2 = {"Number of Runs Scored": [{'Team_Name': teamName, 'Number Of Scored Runs': ScoredRun,'Number Of Conceded Runs':ConcededRun}]}
    #records = json.dumps(list2, indent=4)
    conn.close()
    return json.dumps(finallist)


################ Pie chart showing No of wins,losses,No result matches

#Done
@app.route("/iplviz/team/numberofwinlossnoresult/<id>/<yr>")
def team_getnumberofwinlossnoresult(id,yr):
    #conn_string = "host='localhost' dbname='ipldata-dv' user='postgres' password='piyush'"
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    cursor3 = conn.cursor()
    teamId = id
    year = yr
    cursor.execute('select "Season_Id" from season where "Season_Year"=%s', (str(year),))
    season = cursor.fetchone()
    seasonId = season[0]
    cursor1.execute('select count(*) from "match" where ("Team_Name_Id"=%s or "Opponent_Team_Id"=%s) and "Match_Winner_Id"=%s and "Season_Id"=%s;',(str(teamId),str(teamId),str(teamId),str(seasonId)))
    cursor2.execute('select count(*) from "match" where ("Team_Name_Id"=%s or "Opponent_Team_Id"=%s) and "Match_Winner_Id" not in (%s,0) and "Season_Id"=%s;',(str(teamId),str(teamId),str(teamId),str(seasonId)))
    cursor3.execute('select count(*) from "match" where ("Team_Name_Id"=%s or "Opponent_Team_Id"=%s) and "Match_Winner_Id"=0 and "Season_Id"=%s;',(str(teamId),str(teamId),str(seasonId)))
    result1 = cursor1.fetchone()
    result2 = cursor2.fetchone()
    result3 = cursor3.fetchone()
    numOfWins = result1[0]
    numOfLosses = result2[0]
    numOfNoResult = result3[0]
    #list2 = {}
    #list2 = {"Number of Wins Losses No_Result": [{'Team Name': teamName, 'Number Of Wins': numOfWins,'Number of losses':numOfLosses,'Number of No result':numOfNoResult}]}
    teamwins=[]
    #for i in result:
    x={}
    #x['Team_Name']=teamName
    x['Wins']=numOfWins
    x['Loss']=numOfLosses
    x['No_Result']=numOfNoResult
    teamwins.append(x);
    #records = json.dumps(list2, indent=4)
    conn.close()
    return json.dumps(teamwins)


######################## Pie chart showing split up of won matches as Batting 1st,2nd

#Done
@app.route("/iplviz/team/toss/<id>/<yr>")
def team_toss(id,yr):
    #conn_string = "host='localhost' dbname='ipldata-dv' user='postgres' password='piyush'"
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor1 =conn.cursor()
    #teamName = "Kolkata Knight Riders"
    #cursor.execute('SELECT "Team_Id" from team where "Team_Name"=%s', (teamName,))
   # team = cursor.fetchone()
    teamId = id
    year = yr
    cursor.execute('select "Season_Id" from season where "Season_Year"=%s', (str(year),))
    season = cursor.fetchone()
    seasonId = season[0]
    cursor.execute('SELECT count(*) as "First_Bat_Win" from "match" WHERE "Match_Winner_Id"= %s and "Season_Id" =%s AND (("Toss_Winner_Id"!=%s and "Toss_Decision"=%s) or ("Toss_Winner_Id"=%s and "Toss_Decision"=%s))',(str(teamId),str(seasonId),str(teamId),"field",str(teamId),"bat"))
    cursor1.execute('SELECT count(*) as "First_Bat_Win" from "match" WHERE "Match_Winner_Id"= %s and "Season_Id" =%s AND (("Toss_Winner_Id"!=%s and "Toss_Decision"=%s) or ("Toss_Winner_Id"=%s and "Toss_Decision"=%s))',(str(teamId),str(seasonId),str(teamId),"bat",str(teamId),"field"))
    result = cursor.fetchone()
    result1 = cursor1.fetchone()
    teamwins = []
    #for i in result:
    x={}
    x['BatWins']=int(result[0])
    x['BowlWins']=int(result1[0])
    teamwins.append(x);

   # list2.append({"BatWin": [{'Team_Name': teamName, 'No_Of_Bat_Win': result[0]}]})
   # list2.append({"BowlWin": [{'Team_Name': teamName, 'No_Of_Bowl_Win': result1[0]}]})
    #records = json.dumps(list2, indent=4)
    conn.close()
    return json.dumps(teamwins)


##########################  STAR Players - batsmen,bowlers,wicketkeepers

#Done
@app.route("/iplviz/team/starperformer/<id>/<yr>")
def team_getstarPerformer(id,yr):
    #conn_string = "host='localhost' dbname='ipldata-dv' user='postgres' password='piyush'"
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    teamId = id
    year = yr
    cursor.execute('select "Season_Id" from season where "Season_Year"=%s', (str(year),))
    season = cursor.fetchone()
    seasonId = season[0]
    cursor.execute('select "Player_Name","Striker_Id",sum("Batsman_Scored") from ball_by_ball,player where ball_by_ball."Striker_Id"=player."Player_Id" and "Season_Id"='+str(seasonId)+' and "Team_Batting_Id"='+str(teamId)+' group by "Striker_Id","Player_Name" order by sum("Batsman_Scored") desc limit 1;')
    cursor1.execute('select "Player_Name","Bowler_Id",count(*) from ball_by_ball,player where ball_by_ball."Bowler_Id"=player."Player_Id" and "Season_Id"='+str(seasonId)+' and "Team_Bowling_Id"='+str(teamId)+' and "Dismissal_Type" in (\'caught\',\'caught and bowled\',\'bowled\',\'stumped\',\'lbw\',\'hit wicket\')  group by "Bowler_Id","Player_Name" order by count(*) desc limit 1;')
    # cursor2.execute('select "Player_Name","Player_Id" from "player" where "Player_Id" =(select "Fielder_Id" from "ball_by_ball" where "Dismissal_Type" not in (%s,%s,%s) and "Fielder_Id" in (select DISTINCT "player_id" from "match_player" where "team_id"=%s and "Season_Id"=%s and "is_keeper"=1) group by "Fielder_Id" order by count(*) desc limit 1)',(" ","retired hurt","Bowled",str(teamId),str(seasonId)))
    result = cursor.fetchone()
    result1 = cursor1.fetchone()
    # result2 = cursor2.fetchone()
    finallist=[]
    list2 = {}
    list2['Best_Batsman']=result[0]
    list2['Best_Batsman_Id']=result[1]
    list2['Runs']=result[2]
    list2['Best_Bowler']=result1[0]
    list2['Best_Bowler_Id']=result1[1]
    list2['Wickets']=result1[2]
    finallist.append(list2)
    #list2 = {"Star Performer": [{'Season': year,'Team Name':teamName, 'Best Batsman': result[0],'Best Batsman Id': result[1],'Best Bowler': result1[0],'Best Bowler Id': result1[1],'Best WicketKeeper':result2[0],'Best WicketKeeper Id':result2[1]}]}
    records = json.dumps(finallist)
    conn.close()
    return records


######################## Line chart showing the batting performance of team in 20 overs

#Done
@app.route("/iplviz/team/performance/<id>/<yr>")
def team_getteambattingperformance(id,yr):
    #conn_string = "host='localhost' dbname='ipldata-dv' user='postgres' password='piyush'"
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    teamId = id
    year = yr
    cursor.execute('select "Season_Id" from season where "Season_Year"=%s', (str(year),))
    season = cursor.fetchone()
    seasonId = season[0]
    cursor.execute('select "Over_Id",(CAST( sum("Batsman_Scored")+sum("Extra_Runs")as float)/(CAST (count(*) as float)))*6 as "Total_Runs" from "ball_by_ball" where "Season_Id" = %s and "Match_Id" in (select DISTINCT "match_id" from "match_player" where "Season_Id" = '+str(seasonId)+' and "team_id" = %s) and "Team_Batting_Id" = %s group by "Over_Id" order by "Over_Id"',(str(seasonId),str(teamId),str(teamId)))
    result = cursor.fetchall()
    battingperformance=[]
    for i in result:
        x={}
        x['Over_Id']=int(i[0])
        x['Rate']=float(i[1])
        battingperformance.append(x);
    cursor.execute('select "Over_Id",(CAST( sum("Batsman_Scored")+sum("Extra_Runs")as float)/(CAST (count(*) as float)))*6 as "Total_Runs" from "ball_by_ball" where "Season_Id" = %s and "Match_Id" in (select DISTINCT "match_id" from "match_player" where "Season_Id" = '+str(seasonId)+' and "team_id" = %s) and "Team_Bowling_Id" = %s group by "Over_Id" order by "Over_Id"',(str(seasonId),str(teamId),str(teamId)))
    result = cursor.fetchall()
    bowlingperformance=[]
    for i in result:
        x={}
        x['Over_Id']=int(i[0])
        x['Rate']=float(i[1])
        bowlingperformance.append(x);
    loop=0
    finallist=[]
    while loop < len(battingperformance):
        k={}
        k['Over_Id']=battingperformance[loop]['Over_Id']
        k['Run_Rate']=battingperformance[loop]['Rate']
        k['Econ_Rate']=bowlingperformance[loop]['Rate']
        finallist.append(k)
        loop+=1
    records = json.dumps(finallist)
    conn.close()
    return records



#DOne
@app.route("/iplviz/team/getAllMatchesPlayed/<id>/<yr>")
def team_getAllMatchesPlayed(id,yr):
    #conn_string = "host='localhost' dbname='ipldata-dv' user='postgres' password='piyush'"
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    # teamName = "Kolkata Knight Riders"
    # cursor.execute('SELECT "Team_Id" from team where "Team_Name"=%s',(teamName,))
    # team = cursor.fetchone()
    teamId = id
    year = yr
    cursor.execute('select "Season_Id" from season where "Season_Year"=%s', (str(year),))
    season = cursor.fetchone()
    seasonId = season[0]
    cursor.execute('select "Match_Id" , "Team_Name_Id","Opponent_Team_Id" from match where "Match_Id" in (select DISTINCT "match_id" from "match_player" where "Season_Id" = %s and "team_id" = %s)',(str(seasonId),str(teamId)))
    result = cursor.fetchall()
    list2 = []
    for i in result:
        x={}
        x['Match_Id']=i[0]
        x['Team_Id']=int(i[1])
        x['Opponent_Id'] = int(i[2])
        list2.append(x)
    j = 0
    y = []
    z = []
    while j < len(list2):
        y.append(list2[j]['Team_Id'])
        z.append(list2[j]['Opponent_Id'])
        j += 1

    team1 = []
    for id in y:
        cursor.execute('select "Team_Name" from team where "Team_Id"=' + str(id) + '')
        result = cursor.fetchall()
        for i in result:
            team1.append(i[0])
    team2 = []
    for id in z:
        cursor.execute('select "Team_Name" from team where "Team_Id"=' + str(id) + '')
        result = cursor.fetchall()
        for i in result:
            team2.append(i[0])
    finallist = []
    loop = 0
    while loop < len(team1):
        k = {}
        k['Team_Id'] = list2[loop]['Team_Id']
        k['Opponent_Id'] = list2[loop]['Opponent_Id']
        k['Team1_Name'] = team1[loop]
        k['Team2_Name'] = team2[loop]
        k['Match_Id'] = list2[loop]['Match_Id']
        finallist.append(k)
        loop += 1
    cursor.close()
    conn.close()
    return json.dumps(finallist)

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)