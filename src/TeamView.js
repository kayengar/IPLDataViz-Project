import React, {Component} from 'react';
import ReactHighcharts from 'react-highcharts';
import axios from 'axios';
import {Reactbootstrap,Table, Button, ButtonGroup, Grid, Row, Col, Nav, NavItem} from 'react-bootstrap';
import AppHeader from './AppHeader'
import TeamPerformance from './team/TeamPerformance'
import TeamResults from './team/TeamResults'
import TeamToss from './team/TeamToss'
import TeamPosition from './team/TeamPosition'
import {browserHistory} from 'react-router'

const apiURL = 'http://localhost:5000/iplviz/team'
const matchListURL = 'getAllMatchesPlayed'
const starPerformer = 'starperformer'
const teamPosition = 'positionofteam'

class TeamView extends Component {
    constructor(props) {
        super(props);
        this.state = {
            teamList: [],
            teamName: '',
            playerList: [],
            matchList: [],
            starperfList: [],
            teamPosition: []
        }
        this.handlePlayer = this.handlePlayer.bind(this)
        // this.handleMatch = this.handleMatch.bind(this)
    }

    componentWillMount() {
        let seasonYr = sessionStorage.seasonYear
        let teamid = sessionStorage.teamid
        this.loadPlayerList(teamid,seasonYr)
        this.loadMatchList(teamid,seasonYr)
        this.loadStarPlayerTable(teamid,seasonYr)
        this.loadTeamPosition(teamid)
    }

    loadPlayerList(teamid, seasonYear) {
        axios.get(`${apiURL}/${teamid}/${seasonYear}`)
        .then(res => {
            console.log('playerList', res.data)
            this.setState({playerList: res.data})
        })
    }

    loadMatchList(teamid, seasonYear) {
        axios.get(`${apiURL}/${matchListURL}/${teamid}/${seasonYear}`)
        .then(res => {
            this.setState({matchList: res.data})
        })
    }

    loadStarPlayerTable(teamid, seasonYear) {
        axios.get(`${apiURL}/${starPerformer}/${teamid}/${seasonYear}`)
        .then(res => {
            this.setState({starperfList: res.data[0]})
        })
    }

    loadTeamPosition(teamid) {
        axios.get(`${apiURL}/${teamPosition}/${teamid}`)
        .then(res => {
            console.log('Team Position', res.data)
            this.setState({teamPosition: res.data})
        })
    }

    // teamName(data, id) {
    //     let tName
    //     data.map(function(val){
    //         console.log(val.Team_Id, id)
    //         if(val.Team_Id === parseInt(id)) {
    //             tName = val.Team_Name
    //         }
    //     })
    //     return tName
    // }
    handlePlayer(k, e) {
      let pId = e.target.getAttribute('data-attr')
      sessionStorage.setItem('playerId', parseInt(pId))
      browserHistory.push('/playerDetails')
    }
    
    handleMatch(k, e) {
      let mId = e.target.getAttribute('data-matchid')
      let mName = e.target.text
      sessionStorage.setItem('matchId', parseInt(mId))
      sessionStorage.setItem('matchName', mName)
      browserHistory.push('/matchDetails')
    }

    playerList() {
      let pList = this.state.playerList
      return(
          <div className="container-fluid">
            <Nav bsStyle="pills" stacked onSelect={this.handlePlayer}>
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
      let mList = this.state.matchList
      return(
          <div className="container-fluid">
            <Nav bsStyle="pills" stacked onSelect={this.handleMatch}>
                {
                    mList.map(function(o,i){
                        return(<NavItem eventKey={i+1} key={i+1} data-matchid={o.Match_Id}>{o.Team1_Name} vs {o.Team2_Name}</NavItem>)
                    })
                }
            </Nav>
          </div>
      )
    }

    starPerformerTable() {
        let tableData = this.state.starperfList
        console.log(tableData)
        return ( 
            <div>
                <h3>Star Performers Table</h3>
                <Table striped bordered condensed hover>
                    <thead>
                        <tr>
                            <th>Best Batsmen</th>
                            <th>Best Bowler</th>
                            {/*<th>Best Wicketkeeper</th>                    */}
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{tableData.Best_Batsman}</td>
                            <td>{tableData.Best_Bowler}</td>
                            {/*<td>{tableData.Best_WicketKeeper}</td>*/}
                        </tr>
                </tbody>
                </Table>
            </div>
        )
    }

    renderPerformanceGraph(id, yr) {
        return (
            <TeamPerformance urlExt={apiURL} teamid={id} seasonYear={yr}/>
        )    
    }

    renderTeamResultsGraph(id, yr) {
        return (
            <TeamResults urlExt={apiURL} teamid={id} seasonYear={yr}/>
        )
    }

    renderTeamTossGraph(id, yr) {
        return (
            <TeamToss urlExt={apiURL} teamid={id} seasonYear={yr}/>
        )
    }

    renderTeamPosition(id, yr) {
        return (
            <TeamPosition urlExt={apiURL} teamid={id} seasonYear={yr}/>
        )
    }
    

    render() {
        let {teamid, seasonYear} = sessionStorage
        // let tName = this.teamName(teamid)
        return (
            <div className='team-container'>
                <AppHeader/>
                <h3>{sessionStorage.teamName}-{seasonYear}</h3>
                <Grid>
                    <Row className="show-grid">
                        <Col xs={4} md={2}>
                            <h3>Player Names</h3>
                            {this.playerList()}
                        </Col>
                        <Col xs={10} md={8}>
                            {this.starPerformerTable()}
                            {this.renderTeamPosition(teamid, seasonYear)}
                            {this.renderPerformanceGraph(teamid, seasonYear)}
                            {this.renderTeamResultsGraph(teamid, seasonYear)}
                            {this.renderTeamTossGraph(teamid, seasonYear)}
                        </Col>
                        <Col xs={4} md={2}>
                            <h3>Matches</h3>
                            {this.matchList()}
                        </Col>
                    </Row>
                </Grid>
            </div>
        )
    }
}

export default TeamView;