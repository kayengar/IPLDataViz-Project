import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import {Reactbootstrap, Table} from 'react-bootstrap';
import axios from 'axios';
import '../OldFiles/Runrateviz.css';

const pointsUrl = 'season/pointstable'
const topBatsmanUrl = 'season/top3batsmen'
const topBowlersUrl = 'season/top3bowlers'

class SeasonTables extends Component {
  constructor(props) {
      super(props);
      this.state = {
          pointsdata: [],
          topbatsmendata: [],
          topbowlersdata: [],
          currentYr: 2008
      }
      this.loadPointsTableData = this.loadPointsTableData.bind(this);
      this.renderPointsTable = this.renderPointsTable.bind(this);
  }

  componentWillMount() {
      this.loadPointsTableData(pointsUrl);
      this.loadTopBatsmenData(topBatsmanUrl);
      this.loadTopBowlersData(topBowlersUrl);
      console.log('in')
  }

//   shouldComponentUpdate(nextProps) {
//     console.log("---------------------------------------------------------", this.props.currentYr,  nextProps.currentYr)
//     return (this.props.currentYr !== nextProps.currentYr)
//   }

  loadPointsTableData(url) {
      axios.get(`${this.props.urlExt}/${url}/${this.props.currentYr}`)
        .then(res => {
            console.log("Tables",res.data)
            this.setState({pointsdata: res.data, currentYr: this.props.currentYr})
        })
  }

  loadTopBatsmenData(url) {
      axios.get(`${this.props.urlExt}/${url}/${this.props.currentYr}`)
        .then(res => {
            console.log("Tables",res.data)
            this.setState({topbatsmendata: res.data, currentYr: this.props.currentYr})
        })
  }

  loadTopBowlersData(url) {
      axios.get(`${this.props.urlExt}/${url}/${this.props.currentYr}`)
        .then(res => {
            console.log("Tables",res.data)
            this.setState({topbowlersdata: res.data, currentYr: this.props.currentYr})
        })
  }

  renderPointsTable() {
    let tableData = this.state.pointsdata;
    tableData.sort(function(a,b){
        return b.Points - a.Points;
    })
    // let winner = 
    console.log("Here", tableData)
    return (  
        <Table striped bordered condensed hover>
            <thead>
                <tr>
                    <th>Team Name</th>
                    <th>Points</th>
                </tr>
            </thead>
        <tbody>
            {
                tableData.map(function(o,i){
                    if(o.Wins) {
                        return (
                            <tr key={i+1}>
                                <td>{o.Team_Name}</td>
                                <td>{o.Points}</td>
                            </tr>
                        )
                    }
                })
            }
        </tbody>
    </Table>
    )
  }

  top3batsmen() {
    let tableData = this.state.topbatsmendata;
    tableData.sort(function(a,b){
        return b.Runs - a.Runs;
    })
    // let winner = 
    console.log("Here", tableData)
    return (  
        <Table striped bordered condensed hover>
            <thead>
                <tr>
                    <th>Player Name</th>
                    <th>Runs</th>
                </tr>
            </thead>
        <tbody>
            {
                tableData.map(function(o,i){
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
    )
  }

top3bowlers() {
    let tableData = this.state.topbowlersdata;
    tableData.sort(function(a,b){
        return b.Wickets - a.Wickets;
    })
    // let winner = 
    console.log("Here", tableData)
    return (  
        <Table striped bordered condensed hover>
            <thead>
                <tr>
                    <th>Player Name</th>
                    <th>Wickets</th>
                </tr>
            </thead>
        <tbody>
            {
                tableData.map(function(o,i){
                    return (
                        <tr key={i+1}>
                            <td>{o.Player_Name}</td>
                            <td>{o.Wickets}</td>
                        </tr>
                    )
                })
            }
        </tbody>
    </Table>
    )
  }

  render() {
    let gData = this.state.data
    return (
      <div className="season_tables">
          <div className="points_table">
            <h3>Points Table</h3>
            {this.renderPointsTable()}
          </div>
          <div className="top3batsmen_table">
            <h3>Top 3 Batsmen</h3>
            {this.top3batsmen()}
          </div>
          <div className="top3bowlers_table">
            <h3>Top 3 Bowlers</h3>
            {this.top3bowlers()}
          </div>
      </div>
    );
  }
}

export default SeasonTables;
