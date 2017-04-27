import React, {Component} from 'react';
import ReactHighcharts from 'react-highcharts';
import axios from 'axios';
import {Reactbootstrap,Table, Button, ButtonGroup, Grid, Row, Col, Nav, NavItem} from 'react-bootstrap';
import AppHeader from './AppHeader'
// import './MatchDetails.css'
import RunrateViz from './match/RunrateViz'
import Team1Split from './match/Team1Split'
import Team1WSplit from './match/Team1WSplit'
import Team2Split from './match/Team2Split'
import Team2WSplit from './match/Team2WSplit'

const apiURL = 'http://localhost:5000/iplviz/match'
const teamoneTopbatsman = 't1topbatsmen' 
const teamtwoTopbatsman = 't2topbatsmen' 
const teamoneTopbowlers = 't1topbowlers' 
const teamtwoTopbowlers = 't2topbowlers' 

class MatchDetails extends Component {
    constructor(props) {
        super(props);
        this.state = {
            playerDetails: []
        }
    }

    // shouldComponentUpdate(nextProps, nextState) {
    //     return this.state.playerDetails !== nextState.playerDetails
    // }

    componentWillMount() {
        let playerId = sessionStorage.getItem('playerId')
        // this.getTeamOneBatsmen()
        // this.getTeamOneBowler()
        // this.getTeamTwoBatsmen()
        // this.getTeamTwoBowler()         
    }

    // getPlayerDetails(pId) {
    //     axios.get(`${apiURL}/${playerdetails}/${pId}`)
    //     .then(res => {
    //         console.log('playerDetails', res.data)
    //         this.setState({playerDetails: res.data[0]})
    //     })
    // }

    render() {
        let matchId = sessionStorage.getItem('matchId')
        return (
            <div className='match-container'>
                <AppHeader/>
                <Grid>
                    <Row className="show-grid">
                        <Col xs={8} md={12}>
                            {<RunrateViz urlExt={apiURL} mId={matchId}/>}
                            {<Team1Split urlExt={apiURL} mId={matchId}/>}
                            {<Team1WSplit urlExt={apiURL} mId={matchId}/>}
                            {<Team2Split urlExt={apiURL} mId={matchId}/>}                            
                            {<Team2WSplit urlExt={apiURL} mId={matchId}/>}
                        </Col>
                    </Row>
                </Grid>
            </div>
        )
    }
}

export default MatchDetails;