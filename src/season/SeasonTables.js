import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import {Reactbootstrap, Table} from 'react-bootstrap';
import axios from 'axios';
import '../match/Runrateviz.css';

const pointsUrl = 'season/pointstable'
const topBatsmanUrl = 'season/top3batsmen'
const topBowlersUrl = 'season/top3bowlers'
const topKeepersUrl = 'season/top3keepers'
const topPartnershipUrl = 'season/top3partnership'

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
      this.loadTopKeepersData(topKeepersUrl);
      this.loadPartnershipData(topPartnershipUrl);
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

  loadTopKeepersData(url) {
      axios.get(`${this.props.urlExt}/${url}/${this.props.currentYr}`)
        .then(res => {
            console.log('Top Keepers',res.data)
            this.setState({topkeepersdata: res.data, currentYr: this.props.currentYr})
        })
  }

  loadPartnershipData(url) {
      axios.get(`${this.props.urlExt}/${url}/${this.props.currentYr}`)
        .then(res => {
            console.log('Top Partnership', res.data)
            this.setState({toppartnershipdata: res.data, currentYr: this.props.currentYr})
        })
  }

  renderPointsTable() {
    let tableData = this.state.pointsdata;
    tableData.sort(function(a,b){
        return b.Points - a.Points;
    })
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

  top3keepers() {
    let tableData = this.state.topkeepersdata ? this.state.topkeepersdata : [];

    return (  
        <Table striped bordered condensed hover>
            <thead>
                <tr>
                    <th>Player Name</th>
                    <th>Dismissals</th>
                </tr>
            </thead>
        <tbody>
            {
                tableData.map(function(o,i){
                    return (
                        <tr key={i+1}>
                            <td>{o.Player_Name}</td>
                            <td>{o.Dismissals}</td>
                        </tr>
                    )
                })
            }
        </tbody>
    </Table>
    )
  }

  top3partnership() {
    let tableData = this.state.toppartnershipdata ? this.state.toppartnershipdata : [];

    return (  
        <Table striped bordered condensed hover>
            <thead>
                <tr>
                    <th>Player One Name</th>
                    <th>Player Two Name</th>
                    <th>Runs</th>
                </tr>
            </thead>
        <tbody>
            {
                tableData.map(function(o,i){
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
    )
  }
  render() {
    let gData = this.state.data
    return (
    <div className="seasontable-container">
      <div className="tables_left">
          <div className="points_table">
            <h3>Points Table</h3>
            {this.renderPointsTable()}
          </div>
      </div>
      <div className="tables_right">
        <div className="top3batsmen_table">
                <h3>Top 3 Batsmen</h3>
                {this.top3batsmen()}
        </div>
        <div className="top3bowlers_table">
                <h3>Top 3 Bowlers</h3>
                {this.top3bowlers()}
        </div>
        <div className="top3keepers_table">
                <h3>Top 3 Keepers</h3>
                {this.top3keepers()}
        </div>
        <div className="top3partnership_table">
                <h3>Top 3 Partnerships</h3>
                {this.top3partnership()}
        </div>
      </div>
    </div>
    );
  }
}

export default SeasonTables;
