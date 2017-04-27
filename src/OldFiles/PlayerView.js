import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import {Reactbootstrap, Table} from 'react-bootstrap';
import axios from 'axios';
import './Runrateviz.css';

const pointsUrl = 'season/pointstable'
const topBatsmanUrl = 'season/top3batsmen'
const topBowlersUrl = 'season/top3bowlers'

class PlayerView extends Component {
  constructor(props) {
      super(props);
      this.state = {
          playerdata: [{"Player_Name": "JH Kallis", "Country": "South Africa", "Season_Id": 1, "Season_Year": 2008, "Batsman_Scored": 199, "Player_Id": 9}, {"Player_Name": "JH Kallis", "Country": "South Africa", "Season_Id": 2, "Season_Year": 2009, "Batsman_Scored": 361, "Player_Id": 9}, {"Player_Name": "JH Kallis", "Country": "South Africa", "Season_Id": 3, "Season_Year": 2010, "Batsman_Scored": 572, "Player_Id": 9}, {"Player_Name": "JH Kallis", "Country": "South Africa", "Season_Id": 4, "Season_Year": 2011, "Batsman_Scored": 424, "Player_Id": 9}, {"Player_Name": "JH Kallis", "Country": "South Africa", "Season_Id": 5, "Season_Year": 2012, "Batsman_Scored": 409, "Player_Id": 9}, {"Player_Name": "JH Kallis", "Country": "South Africa", "Season_Id": 6, "Season_Year": 2013, "Batsman_Scored": 311, "Player_Id": 9}, {"Player_Name": "JH Kallis", "Country": "South Africa", "Season_Id": 7, "Season_Year": 2014, "Batsman_Scored": 151, "Player_Id": 9}]
      }
      this.loadPointsTableData = this.loadPointsTableData.bind(this);
      this.renderPointsTable = this.renderPointsTable.bind(this);
  }

  componentWillMount() {
    //   this.loadPointsTableData(pointsUrl);
    //   this.loadTopBatsmenData(topBatsmanUrl);
    //   this.loadTopBowlersData(topBowlersUrl);
  }

//   shouldComponentUpdate(nextProps) {
//     return (this.props.currentYr !== nextProps.currentYr)
//   }

  loadPointsTableData(url) {
      axios.get(`${this.props.urlExt}/${url}/${this.props.currentYr}`)
        .then(res => {
            this.setState({pointsdata: res.data, currentYr: this.props.currentYr})
        })
  }

  loadTopBatsmenData(url) {
      axios.get(`${this.props.urlExt}/${url}/${this.props.currentYr}`)
        .then(res => {
            this.setState({topbatsmendata: res.data, currentYr: this.props.currentYr})
        })
  }

  loadTopBowlersData(url) {
      axios.get(`${this.props.urlExt}/${url}/${this.props.currentYr}`)
        .then(res => {
            this.setState({topbowlersdata: res.data, currentYr: this.props.currentYr})
        })
  }

  renderPointsTable() {
    let tableData = this.state.playerdata;
    // let winner = 
    return(
        <div>
            <h4>Player Name: {tableData[0].Player_Name}</h4>
            <h4>Country: {tableData[0].Country}</h4>
        </div>
    )
  }

  renderTeamOneData() {
      let table1Data = [{"Player_Id": 14, "Runs": 18, "Player_Name": "P Kumar"}, {"Player_Id": 13, "Runs": 9, "Player_Name": "AA Noffke"}, {"Player_Id": 9, "Runs": 8, "Player_Name": "JH Kallis"}]
            let table2Data = [{"Player_Id": 9, "Player1_Name": "JH Kallis", "Runs": 52, "Wickets": 1}, {"Player_Id": 13, "Player1_Name": "AA Noffke", "Runs": 41, "Wickets": 1}, {"Player_Id": 15, "Player1_Name": "Z Khan", "Runs": 38, "Wickets": 1}]
      let table3Data = [{"Player2_Name": "JH Kallis", "Player1_Name": "W Jaffer", "Player2_Id": 9, "Runs": 15, "Player1_Id": 7}, {"Player2_Name": "P Kumar", "Player1_Name": "AA Noffke", "Player2_Id": 14, "Runs": 14, "Player1_Id": 13}, {"Player2_Name": "MV Boucher", "Player1_Name": "CL White", "Player2_Id": 11, "Runs": 14, "Player1_Id": 10}]
      return (
        <div> 
            <Table striped bordered condensed hover>
                    <thead>
                        <tr>
                            <th>Player Name</th>
                            <th>Runs</th>
                        </tr>
                    </thead>
                <tbody>
                    {
                        table1Data.map(function(o,i){
                                return (
                                    <tr key={i+1}>
                                        <td>{o.Player_Name}</td>
                                        <td>{o.Runs}</td>
                                    </tr>
                                )
                        })
                    }
                </tbody>
            </Table>
            <Table striped bordered condensed hover>
                    <thead>
                        <tr>
                            <th>Player Name</th>
                            <th>Wickets</th>
                        </tr>
                    </thead>
                <tbody>
                    {
                        table2Data.map(function(o,i){
                                return (
                                    <tr key={i+1}>
                                        <td>{o.Player1_Name}</td>
                                        <td>{o.Wickets}</td>
                                    </tr>
                                )
                        })
                    }
                </tbody>
            </Table>
            <Table striped bordered condensed hover>
                    <thead>
                        <tr>
                            <th>Player One</th>
                            <th>Player Two</th>
                            <th>Runs</th>
                        </tr>
                    </thead>
                <tbody>
                    {
                        table3Data.map(function(o,i){
                                return (
                                    <tr key={i+1}>
                                        <td>{o.Player1_Name}</td>
                                        <td>{o.Player2_Name}</td>
                                        <td>{o.Runs}</td>
                                    </tr>
                                )
                        })
                    }
                </tbody>
            </Table>
        </div>
    )
}

  renderTeamTwoData() {
      let table1Data = [{"Player_Id": 2, "Runs": 158, "Player_Name": "BB McCullum"}, {"Player_Id": 3, "Runs": 20, "Player_Name": "RT Ponting"}, {"Player_Id": 4, "Runs": 12, "Player_Name": "DJ Hussey"}]
      let table2Data = [{"Player_Id": 82, "Player1_Name": "AB Agarkar", "Runs": 25, "Wickets": 3}, {"Player_Id": 1, "Player1_Name": "SC Ganguly", "Runs": 23, "Wickets": 2}, {"Player_Id": 106, "Player1_Name": "AB Dinda", "Runs": 9, "Wickets": 2}]
      let table3Data = [{"Player2_Name": "BB McCullum", "Player1_Name": "SC Ganguly", "Player2_Id": 2, "Runs": 61, "Player1_Id": 1}, {"Player2_Name": "DJ Hussey", "Player1_Name": "BB McCullum", "Player2_Id": 4, "Runs": 60, "Player1_Id": 2}, {"Player2_Name": "RT Ponting", "Player1_Name": "BB McCullum", "Player2_Id": 3, "Runs": 51, "Player1_Id": 2}]
      return (
        <div> 
            <Table striped bordered condensed hover>
                    <thead>
                        <tr>
                            <th>Player Name</th>
                            <th>Runs</th>
                        </tr>
                    </thead>
                <tbody>
                    {
                        table1Data.map(function(o,i){
                                return (
                                    <tr key={i+1}>
                                        <td>{o.Player_Name}</td>
                                        <td>{o.Runs}</td>
                                    </tr>
                                )
                        })
                    }
                </tbody>
            </Table>
            <Table striped bordered condensed hover>
                    <thead>
                        <tr>
                            <th>Player Name</th>
                            <th>Wickets</th>
                        </tr>
                    </thead>
                <tbody>
                    {
                        table2Data.map(function(o,i){
                                return (
                                    <tr key={i+1}>
                                        <td>{o.Player1_Name}</td>
                                        <td>{o.Wickets}</td>
                                    </tr>
                                )
                        })
                    }
                </tbody>
            </Table>
            <Table striped bordered condensed hover>
                    <thead>
                        <tr>
                            <th>Player One</th>
                            <th>Player Two</th>
                            <th>Runs</th>
                        </tr>
                    </thead>
                <tbody>
                    {
                        table3Data.map(function(o,i){
                                return (
                                    <tr key={i+1}>
                                        <td>{o.Player1_Name}</td>
                                        <td>{o.Player2_Name}</td>
                                        <td>{o.Runs}</td>
                                    </tr>
                                )
                        })
                    }
                </tbody>
            </Table>
        </div>
    )
}
  render() {
    let gData = this.state.data
    return (
      <div className="season_tables">
          <div className="player_details">
              <h3>Match Details</h3>
            {/*{this.renderPointsTable()}*/}
            <div>
                <h3>Team One Data</h3>
                {this.renderTeamOneData()}
            </div>
            <div>
                <h3>Team Two Data</h3>
                {this.renderTeamTwoData()}
            </div>
          </div>
      </div>
    );
  }
}

export default PlayerView;
