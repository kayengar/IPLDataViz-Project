import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import {Reactbootstrap,Table, Button, ButtonGroup, Grid, Row, Col, Nav, NavItem} from 'react-bootstrap';
import './SeasonView.css'
import axios from 'axios';
import configMap from './config.js';
import SeasonBoundRuns from './season/SeasonBoundRuns'
import SeasonTables from './season/SeasonTables'
import TeamWinsViz from './season/TeamWinsViz'
import createHistory from 'history/createBrowserHistory'
import {browserHistory} from 'react-router'

const URLExt = 'season/teams'
const playerlistURL = 'team'

class SeasonView extends Component {
  constructor(props) {
      super(props);
      this.state = {
          teamList: [],
          defaultYear: 2008,
          isTeamBtn: true,
          currentYr: 2008,
          isTeamView: false,
          playerList: [ { "Player_Id": 1, "Player_Name": "SC Ganguly" }, { "Player_Id": 2, "Player_Name": "BB McCullum" }, { "Player_Id": 3, "Player_Name": "RT Ponting" }, { "Player_Id": 4, "Player_Name": "DJ Hussey" }, { "Player_Id": 5, "Player_Name": "Mohammad Hafeez" }, { "Player_Id": 62, "Player_Name": "WP Saha" }, { "Player_Id": 63, "Player_Name": "LR Shukla" }, { "Player_Id": 82, "Player_Name": "AB Agarkar" }, { "Player_Id": 83, "Player_Name": "M Kartik" }, { "Player_Id": 84, "Player_Name": "I Sharma" }, { "Player_Id": 95, "Player_Name": "DB Das" }, { "Player_Id": 103, "Player_Name": "Salman Butt" }, { "Player_Id": 104, "Player_Name": "BJ Hodge" }, { "Player_Id": 105, "Player_Name": "Umar Gul" }, { "Player_Id": 106, "Player_Name": "AB Dinda" }, { "Player_Id": 128, "Player_Name": "A Chopra" }, { "Player_Id": 129, "Player_Name": "T Taibu" }, { "Player_Id": 140, "Player_Name": "Iqbal Abdulla" }, { "Player_Id": 144, "Player_Name": "Shoaib Akhtar" }, { "Player_Id": 174, "Player_Name": "BAW Mendis" } ],
          matchesList: [{"Team1_Name": "Royal Challengers Bangalore", "Team2_Name": "Kolkata Knight Riders", "Team_Id": 2, "Opponent_Id": 1, "Match_Id": 335987}, {"Team1_Name": "Kolkata Knight Riders", "Team2_Name": "Deccan Chargers", "Team_Id": 1, "Opponent_Id": 8, "Match_Id": 335991}, {"Team1_Name": "Chennai Super Kings", "Team2_Name": "Kolkata Knight Riders", "Team_Id": 3, "Opponent_Id": 1, "Match_Id": 335998}, {"Team1_Name": "Kolkata Knight Riders", "Team2_Name": "Mumbai Indians", "Team_Id": 1, "Opponent_Id": 7, "Match_Id": 336002}, {"Team1_Name": "Rajasthan Royals", "Team2_Name": "Kolkata Knight Riders", "Team_Id": 5, "Opponent_Id": 1, "Match_Id": 336005}, {"Team1_Name": "Kings XI Punjab", "Team2_Name": "Kolkata Knight Riders", "Team_Id": 4, "Opponent_Id": 1, "Match_Id": 336008}, {"Team1_Name": "Kolkata Knight Riders", "Team2_Name": "Royal Challengers Bangalore", "Team_Id": 1, "Opponent_Id": 2, "Match_Id": 336015}, {"Team1_Name": "Deccan Chargers", "Team2_Name": "Kolkata Knight Riders", "Team_Id": 8, "Opponent_Id": 1, "Match_Id": 336019}, {"Team1_Name": "Kolkata Knight Riders", "Team2_Name": "Delhi Daredevils", "Team_Id": 1, "Opponent_Id": 6, "Match_Id": 336022}, {"Team1_Name": "Mumbai Indians", "Team2_Name": "Kolkata Knight Riders", "Team_Id": 7, "Opponent_Id": 1, "Match_Id": 336026}, {"Team1_Name": "Kolkata Knight Riders", "Team2_Name": "Chennai Super Kings", "Team_Id": 1, "Opponent_Id": 3, "Match_Id": 336030}, {"Team1_Name": "Kolkata Knight Riders", "Team2_Name": "Rajasthan Royals", "Team_Id": 1, "Opponent_Id": 5, "Match_Id": 336032}, {"Team1_Name": "Kolkata Knight Riders", "Team2_Name": "Kings XI Punjab", "Team_Id": 1, "Opponent_Id": 4, "Match_Id": 336040}],
          starPerfData: [],
          playerDetails: [{"Player_Name": "JH Kallis", "Country": "South Africa", "Season_Id": 1, "Season_Year": 2008, "Batsman_Scored": 199, "Player_Id": 9}, {"Player_Name": "JH Kallis", "Country": "South Africa", "Season_Id": 2, "Season_Year": 2009, "Batsman_Scored": 361, "Player_Id": 9}, {"Player_Name": "JH Kallis", "Country": "South Africa", "Season_Id": 3, "Season_Year": 2010, "Batsman_Scored": 572, "Player_Id": 9}, {"Player_Name": "JH Kallis", "Country": "South Africa", "Season_Id": 4, "Season_Year": 2011, "Batsman_Scored": 424, "Player_Id": 9}, {"Player_Name": "JH Kallis", "Country": "South Africa", "Season_Id": 5, "Season_Year": 2012, "Batsman_Scored": 409, "Player_Id": 9}, {"Player_Name": "JH Kallis", "Country": "South Africa", "Season_Id": 6, "Season_Year": 2013, "Batsman_Scored": 311, "Player_Id": 9}, {"Player_Name": "JH Kallis", "Country": "South Africa", "Season_Id": 7, "Season_Year": 2014, "Batsman_Scored": 151, "Player_Id": 9}]
        }
    this.handleSelect = this.handleSelect.bind(this);
    this.handleLogo = this.handleLogo.bind(this);
    this.handleSeasonButtons = this.handleSeasonButtons.bind(this);
  }

  componentWillMount() {
    this.loadTeamList(this.state.defaultYear);
  }

  loadTeamList(seasonYr) {
      axios.get(`${this.props.urlExt}/${URLExt}/${seasonYr}`)
        .then(res => {
            console.log(res.data)
            this.setState({teamList: res.data, currentYr: seasonYr})
        })
  }

  loadPlayerList(teamName) {
    //   axios.get(`${this.props.urlExt}/${playerlistURL}/${teamName}/${this.state.currentYr}`)
    //     .then(res => {
    //         console.log(res.data)
    //         this.setState({playerList: res.data, isTeamView: true})
    //     })
    this.setState({isTeamView: true})
  }

  loadStarPerformer(url) {
    axios.get(`${this.props.urlExt}/${playerlistURL}/${url}`)
        .then(res => {
            console.log(res.data)
            this.setState({starPerfData: res.data[0], isTeamView: true})
        })
  }

  parseGraphData(res) {
      let innings1 = []
      let innings2 = []
     
      res['Innings1'].forEach(function(val){
          innings1.push(val.Runs)
      })
      res['Innings2'].forEach(function(val){
          innings2.push(val.Runs)
      })
      let tmpArr = []
      tmpArr.push(innings1)
      tmpArr.push(innings2)
      return tmpArr
  }

  handleSelect(k, e) {
      console.log(e.target.text)
      let child = e.target.parentNode.parentElement.children
      for(var i=0; i<child.length;i++){
          child[i].setAttribute('class', '')
      }
      e.target.parentNode.setAttribute('class', 'active')
      this.loadTeamList(e.target.text)
  }

  handleLogo(e) {
    let teamId = e.target.getAttribute('data-attr')
    let teamName = e.target.getAttribute('data-teamname')
    sessionStorage.setItem('teamid', parseInt(teamId))
    sessionStorage.setItem('teamName', teamName)
    sessionStorage.setItem('seasonYear', parseInt(this.state.currentYr))
    browserHistory.push('/teamPage')
    // this.loadPlayerList(teamName)
    // this.loadStarPerformer('starperformer')

  }

  handleSeasonButtons(e) {
      let btnVal = e.target.getAttribute('data-attr')
      if(btnVal === 'teamView') {
          this.setState({isTeamBtn: true})
      } else {
          this.setState({isTeamBtn: false})
      }
  }

  seasonList() {
      let sList = configMap.sList
      return(
          <div className="container-fluid">
            <Nav bsStyle="pills" stacked activeKey={1} onSelect={this.handleSelect}>
                {
                    sList.map(function(o,i){
                        return(<NavItem eventKey={i+1} key={i+1} data-attr={o.id}>{o.name}</NavItem>)
                    })
                }
            </Nav>
          </div>
      )
  }

  playerList() {
      let pList = this.state.playerList
      return(
          <div className="container-fluid">
            <Nav bsStyle="pills" stacked activeKey={1} onSelect={this.handleSelect}>
                {
                    pList.map(function(o,i){
                        return(<NavItem eventKey={i+1} key={i+1} data-attr={o.Player_Id}>{o.Player_Name}</NavItem>)
                    })
                }
            </Nav>
          </div>
      )
  }

  matchList() {
      let mList = this.state.matchesList
      return(
          <div className="container-fluid">
            <Nav bsStyle="pills" stacked activeKey={1} onSelect={this.handleSelect}>
                {
                    mList.map(function(o,i){
                        return(<NavItem eventKey={i+1} key={i+1} data-attr={o.Match_Id}>{o.Team1_Name} vs {o.Team2_Name}</NavItem>)
                    })
                }
            </Nav>
          </div>
      )
  }

  teamView() {
      let tList = configMap.teamLogos
      let teamLogos = this.state.teamList
      let clickHandler = this.handleLogo
      return(
        <div>
            {
                teamLogos.map(function(o,i){
                    return(
                        <div className='teamLogos' key={o.Team_Id} onClick={clickHandler}>
                            <img data-attr={o.Team_Id} data-teamname={o.Team_Name} src={require(`./images/Logos/${o.Team_Id}.png`)}/>
                        </div>
                    )
                })
            }
        </div>
      )
  }

  seasonStatsView() {
      return(
        <div className='seasonStats'>
            <SeasonTables urlExt={this.props.urlExt} currentYr={this.state.currentYr}/>
            <div className='seasonGraphs'>
                <SeasonBoundRuns urlExt={this.props.urlExt} currentYr={this.state.currentYr}/>
                <TeamWinsViz urlExt={this.props.urlExt} currentYr={this.state.currentYr}/>
            </div>
        </div>
      )
  }

  startPerformerTable() {
    let tableData = this.state.starPerfData
    console.log(tableData)
    return (  
        <Table striped bordered condensed hover>
            <thead>
                <tr>
                    <th>Best Batsmen</th>
                    <th>Best Bowler</th>
                    <th>Best Wicketkeeper</th>                    
                </tr>
            </thead>
        <tbody>
            <tr>
                <td>{tableData.Best_Batsman}</td>
                <td>{tableData.Best_Bowler}</td>
                <td>{tableData.Best_WicketKeeper}</td>
            </tr>
       </tbody>
    </Table>
    )
  }

  renderGraph() {
    let graphData = this.state.data;
    let team1 = graphData['Team_One']
    let team2 = graphData['Team_Two']
    let xAxisScale = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
    let result = this.parseGraphData(graphData);
    let config = {
        chart: {
            type: 'line'
        },
        title: {
            text: 'Overall Runs Scored per Over'
        },
        subtitle: {
            text: 'Source: kaggle.com'
        },
        xAxis: {
            categories: xAxisScale,
            title: {
                text: 'Over'
            }
        },
        yAxis: {
            title: {
                text: 'Runs Scored'
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: true
            }
        },
        series: [{
            name: team2,
            data: result[1]
        }, {
            name: team1,
            data: result[0]
        }]
    }
    console.log(result)
    if(result[0].length) {   
        console.log('render') 
        return(<ReactHighcharts config={config} ref='chart'></ReactHighcharts>)
    } else {
        return null
    }
  }

//   componentWillUnmount() {
//     this.refs.chart.destroy();
//   }

  render() {
    return (
        (!this.state.isTeamView) ? 
            <div className="season-container">
                <ButtonGroup onClick={this.handleSeasonButtons}>
                    <Button data-attr="teamView"><h4>Teams</h4></Button>
                    <Button data-attr="seasonView"><h4>Season Statistics</h4></Button>
                </ButtonGroup>
                <Grid>
                    <Row className="show-grid">
                        <Col xs={4} md={2}>
                            <h3>Seasons</h3>
                            {this.seasonList()}
                        </Col>
                        <Col xs={14} md={10}>
                            {(this.state.isTeamBtn) ? 
                                this.teamView() : 
                                this.seasonStatsView()
                            }
                        </Col>
                    </Row>
                </Grid>
            </div> :
            <div className="team-container">
                    <h3>Kolkata Knight Riders | 2008</h3>
                <Grid>
                    <Row className="show-grid">
                        <Col xs={4} md={2}>
                            <h3>Player Names</h3>
                            {this.playerList()}
                        </Col>
                        <Col xs={10} md={8}>
                            <h3>Star Performers Table</h3>
                            {this.startPerformerTable()}
                        </Col>
                        <Col xs={4} md={2}>
                            <h3>Matches</h3>
                            {this.matchList()}
                        </Col>
                    </Row>
                </Grid>
            </div>
    );
  }
}

export default SeasonView;