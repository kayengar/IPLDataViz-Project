import React, {Component} from 'react';
import ReactHighcharts from 'react-highcharts';
import axios from 'axios';
import {Reactbootstrap,Table, Button, ButtonGroup, Grid, Row, Col, Nav, NavItem} from 'react-bootstrap';
import AppHeader from './AppHeader'
import './PlayerDetails.css'
import BatsmanSlog from './player/BatsmanSlog'
import BowlerSlog from './player/BowlerSlog'
import BowlerWickets from './player/BowlerWickets'
import BowlerWicketType from './player/BowlerWicketType'
import PlayerEconRate from './player/PlayerEconRate'
import PlayerStrikeRate from './player/PlayerStrikeRate'
import SeasonRuns from './player/SeasonRuns'
import PlayerBio from './player/PlayerBio'


const apiURL = 'http://localhost:5000/iplviz/player'
const playerdetails = 'playerdetails'

class PlayerDetails extends Component {
    constructor(props) {
        super(props);
        this.state = {
            playerDetails: []
        }
    }

    shouldComponentUpdate(nextProps, nextState) {
        return this.state.playerDetails !== nextState.playerDetails
    }

    componentWillMount() {
        let playerId = sessionStorage.getItem('playerId')
        this.getPlayerDetails(playerId)
    }

    getPlayerDetails(pId) {
        axios.get(`${apiURL}/${playerdetails}/${pId}`)
        .then(res => {
            console.log('playerDetails', res.data)
            this.setState({playerDetails: res.data[0]})
        })
    }

    renderPlayerProfile() {
        let {Player_Name, Batting_Style, Bowling_Style, Country, Dismissals, Wickets, Batsman_Scored} = this.state.playerDetails
        return(
            <div className="container">
                <div className="row">
                    <div className="col-md-offset-5 col-md-10 col-lg-offset-5 col-lg-8">
                    <div className="well profile">
                        <div className="col-sm-12">
                            <div className="col-xs-12 col-sm-12">
                                <h2>{Player_Name}</h2>
                                <p><strong>Runs Scored: </strong> {Batsman_Scored} </p>                                
                                <p><strong>Batting Style: </strong> {(Batting_Style) ? Batting_Style.replace('_',' ') : Batting_Style} </p>
                                <p><strong>Bowling Style: </strong> {Bowling_Style} </p>
                                <p><strong>Country: </strong> {Country} </p>
                                <p><strong>Dismissals: </strong> {Dismissals} </p>
                                <p><strong>Wickets: </strong> {Wickets} </p>                                                                
                                {/*<p><strong>Skills: </strong>
                                    <span className="tags">html5</span> 
                                    <span className="tags">css3</span>
                                    <span className="tags">jquery</span>
                                    <span className="tags">bootstrap3</span>
                                </p>*/}
                            </div>             
                            {/*<div className="col-xs-12 col-sm-4 text-center">
                                <figure>
                                    <img src="https://s.yimg.com/qx/cricket/fufp/images/2962_large-16-1-2011-8e505dcd73dd116671b450f7e4ecb19b.jpg" alt="" class="img-circle img-responsive"/>
                                </figure>
                            </div>*/}
                        </div>            
                    </div>                 
                    </div>
                </div>
            </div>
        )
    }

    render() {
        let playerId = sessionStorage.getItem('playerId')
        console.log('PlayerDetails', this.state.playerDetails)
        return (
            <div className='player-container'>
                <AppHeader/>
                <Grid>
                    <Row className="show-grid">
                        <Col xs={8} md={8}>
                            {/*{this.renderPlayerProfile()}*/}
                            <PlayerBio playerDetails={this.state.playerDetails}/>
                            <BatsmanSlog urlExt={apiURL} pId={playerId}/>
                            <BowlerSlog urlExt={apiURL} pId={playerId}/>
                            <BowlerWickets urlExt={apiURL} pId={playerId}/>
                            <BowlerWicketType urlExt={apiURL} pId={playerId}/>
                            <PlayerEconRate urlExt={apiURL} pId={playerId}/>
                            <PlayerStrikeRate urlExt={apiURL} pId={playerId}/>   
                            <SeasonRuns urlExt={apiURL} pId={playerId}/>  
                        </Col>
                    </Row>
                </Grid>
            </div>
        )
    }
}

export default PlayerDetails;