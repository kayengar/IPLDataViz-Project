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

@app.route("/iplviz/toss")
def toss():
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor1 =conn.cursor()
    cursor.execute('SELECT "Team_Name",count(*) as "First_Bat_Win" from "match_table","team" WHERE "Match_Winner_Id"= "Team_Id" AND "Toss_Winner_Id"!=1 and "Toss_Decision"=%s and "Match_Winner_Id"=1 or "Toss_Winner_Id"=1 and "Toss_Decision"=%s and "Match_Winner_Id"=1 group by "Team_Name"',("field","bat"))
    cursor1.execute('SELECT "Team_Name",count(*) as "First_Bat_Win" from "match_table","team" WHERE "Match_Winner_Id"= "Team_Id" AND "Toss_Winner_Id"!=1 and "Toss_Decision"=%s and "Match_Winner_Id"=1 or "Toss_Winner_Id"=1 and "Toss_Decision"=%s and "Match_Winner_Id"=1 group by "Team_Name"',("bat","field"))
    result = cursor.fetchall()
    result1 = cursor1.fetchall()
    list2 = {}
    list2 = {"BatWin": [{'Team_Name': key, 'No_Of_Bat_Win': value} for key, value in result],
             "FieldWin": [{'Team_Name': key, 'No_Of_Field_Win': value} for key, value in result1]}
    records = json.dumps(list2, indent=4)
    conn.close()
    return records

 #################################Player end points ############### 

@app.route("/iplviz/player/playerwickettype")
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


@app.route("/iplviz/player/playerwicket")
def playerwicket_data():
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute('''SELECT distinct "Player_Name","Season_Year",count("Dismissal_Type") from "ball_by_ball","player","Season" where "Dismissal_Type" not in (' ','run out') and "player"."Player_Id"="ball_by_ball"."Bowler_Id" and "Player_Name"='SL Malinga' and "Season"."Season_Id"="ball_by_ball"."Season_Id" group by "Player_Name","Season_Year" order by "Season_Year" ASC;''')
    playername = cursor.fetchall()
    bowlerStatistics = []
    for i in playername:
        x = {}
        x['Player_Name'] = i[0]
        x['Season_Year'] = i[1]
        x['Count'] = int(i[2])
        bowlerStatistics.append(x)
    cursor.close()
    conn.close()
    return json.dumps(bowlerStatistics)

##########################End of player endpoints##############################

########################### Season endpoints starts here############################
#####Author:KANNAN GANESAN
@app.route("/iplviz/season/teams")
def season_teams():
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = 2008
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


@app.route("/iplviz/season/teamwins")
def season_teamwins():
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = 2008
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

@app.route("/iplviz/season/pointstable")
def points_table():
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = 2008
    queryStr = 'SELECT "Season_Id" from season where "Season_Year"='+str(year)+''
    cursor.execute(queryStr)
    seasons=cursor.fetchall()
    for i in seasons:
        seasonid=int(i[0])
    #cursor1 = conn.cursor()
    cursor.execute('SELECT "Team_Id",team."Team_Name",COUNT(match."Match_Winner_Id")*2 as Points,COUNT(match."Match_Winner_Id") as WON FROM match,team WHERE "Season_Id"='+str(seasonid)+' and team."Team_Id" = match."Match_Winner_Id" GROUP BY team."Team_Name","Team_Id"')
    result=cursor.fetchall()
    #result1=cursor1.fetchall()
    pointstable=[]
    for i in result:
        x={}
        x['Team_Id']=int(i[0])
        x['Points']=int(i[2])
        x['Wins']=int(i[3])
        x['Team_Name']=i[1]
        x['Season_Year']=year
        pointstable.append(x);
    cursor.close()
    conn.close()
    return json.dumps(pointstable)

@app.route("/iplviz/season/top3batsmen")
def season_top3bat():
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = 2008
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

@app.route("/iplviz/season/top3bowlers")
def season_top3bowl():
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = 2008
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

@app.route("/iplviz/season/top3keepers")
def season_top3keepers():
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = 2008
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


@app.route("/iplviz/season/top3partnership")
def season_top3partners():
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = 2008
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
            player1.append(result[0])
    player2=[]
    for id in z:
        cursor.execute('select "Player_Name" from player where "Player_Id"='+str(id)+'')
        result=cursor.fetchall()
        for i in result:
            player2.append(result[0])
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

@app.route("/iplviz/season/teamrunrates")
def season_teamrunrates():
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = 2008
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
    cursor.close()
    conn.close()
    return json.dumps(teamrunrates)

@app.route("/iplviz/season/teameconomyrates")
def season_teameconomyrates():
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = 2008
    queryStr = 'SELECT "Season_Id" from season where "Season_Year"='+str(year)+''
    cursor.execute(queryStr)
    seasons=cursor.fetchall()
    for i in seasons:
        seasonid=int(i[0])
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
    cursor.close()
    conn.close()
    return json.dumps(teameconomyrates)

@app.route("/iplviz/season/teamslogruns")
def season_teamslogruns():
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
    cursor.close()
    conn.close()
    return json.dumps(teamslogruns)

@app.route("/iplviz/season/teamboundruns")
def season_teamboundruns():
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = 2008
    queryStr = 'SELECT "Season_Id" from season where "Season_Year"='+str(year)+''
    cursor.execute(queryStr)
    seasons=cursor.fetchall()
    for i in seasons:
        seasonid=int(i[0])
    cursor.execute('SELECT "Team_Id","Team_Name",sum("Batsman_Scored")+sum("Extra_Runs") from ball_by_ball,team where "Season_Id"='+str(seasonid)+' and ball_by_ball."Team_Batting_Id"=team."Team_Id" group by "Team_Name","Team_Id"')
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
        k['Total_Runs']=totalruns[loop]['Runs']
        k['Bound_Runs']=boundruns[loop]['Runs']
        finallist.append(k)
        loop+=1
    print finallist
    cursor.close()
    conn.close()
    return json.dumps(finallist)

@app.route("/iplviz/season/teamslogrunrates")
def season_teamslogrunrates():
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = 2008
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
    cursor.close()
    conn.close()
    return json.dumps(teamslogrunrates)

@app.route("/iplviz/season/teamslogeconrates")
def season_teamslogeconrates():
    print "Connecting to database\n ->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    year = 2008
    queryStr = 'SELECT "Season_Id" from season where "Season_Year"='+str(year)+''
    cursor.execute(queryStr)
    seasons=cursor.fetchall()
    for i in seasons:
        seasonid=int(i[0])
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
    cursor.close()
    conn.close()
    return json.dumps(teamslogeconrates)

##################################################Season endpoints ends here#############################################
if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)



