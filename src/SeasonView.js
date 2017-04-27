import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import {Reactbootstrap,Table, Button, ButtonGroup, Grid, Row, Col, Nav, NavItem} from 'react-bootstrap';
import './SeasonView.css'
import axios from 'axios';
import configMap from './config.js';
import SeasonBoundRuns from './season/SeasonBoundRuns'
import SeasonTables from './season/SeasonTables'
import TeamWinsViz from './season/TeamWinsViz'
import SeasonSlogRates from './season/SeasonSlogRates'
import SeasonSlogRuns from './season/SeasonSlogRuns'
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
          isTeamView: false
      }
    this.handleSelect = this.handleSelect.bind(this);
    this.handleLogo = this.handleLogo.bind(this);
    this.handleSeasonButtons = this.handleSeasonButtons.bind(this);
  }

  shouldComponentUpdate(nextProps, nextState) {
    return this.state.teamList !== nextState.teamList || this.state.isTeamBtn !== nextState.isTeamBtn || this.state.currentYr !==nextState.currentYr
  }

  componentWillMount() {
    this.loadTeamList(this.state.defaultYear);
  }

  loadTeamList(seasonYr) {
      axios.get(`${this.props.urlExt}/${URLExt}/${seasonYr}`)
        .then(res => {
            this.setState({teamList: res.data, currentYr: seasonYr, isTeamBtn: this.state.isTeamBtn})
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
          console.log('Team Button')
          this.setState({isTeamBtn: true})
      } else {
          console.log('Season Button')
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
      console.log('Season Stats',this.state.currentYr)
      return(
        <div className='seasonStats'>
            <SeasonTables urlExt={this.props.urlExt} currentYr={this.state.currentYr}/>
            <div className='seasonGraphs'>
                <SeasonBoundRuns urlExt={this.props.urlExt} currentYr={this.state.currentYr}/>
                <TeamWinsViz urlExt={this.props.urlExt} currentYr={this.state.currentYr}/>
            </div>
                <SeasonSlogRates urlExt={this.props.urlExt} currentYr={this.state.currentYr}/>
        </div>
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
    if(result[0].length) {   
        return(<ReactHighcharts config={config} ref='chart'></ReactHighcharts>)
    } else {
        return null
    }
  }

  render() {
    return (
            <div className="season-container">
                <ButtonGroup onClick={this.handleSeasonButtons}>
                    <Button data-attr="teamView">Teams</Button>
                    <Button data-attr="seasonView">Season Statistics</Button>
                </ButtonGroup>
                <Grid>
                    <Row className="show-grid">
                        <Col xs={4} md={2}>
                            <h3>Seasons</h3>
                            {this.seasonList()}
                        </Col>
                        <Col xs={14} md={10}>
                            {
                                (this.state.isTeamBtn) ? 
                                    this.teamView() : 
                                    this.seasonStatsView()
                            }
                        </Col>
                    </Row>
                </Grid>
            </div>
    );
  }
}

export default SeasonView;