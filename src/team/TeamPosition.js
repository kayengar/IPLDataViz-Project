import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import {Reactbootstrap, Table} from 'react-bootstrap';
import axios from 'axios'; 

const URLExt = 'positionofteam'

class TeamPosition extends Component {
  constructor(props) {
      super(props);
      this.state = {
          data: []
      }
      this.loadPositionData = this.loadPositionData.bind(this);
  }

  componentWillMount() {
      this.loadPositionData();
  }

  loadPositionData(url) {
      let {teamid, seasonYear} = this.props
      axios.get(`${this.props.urlExt}/${URLExt}/${teamid}`)
        .then(res => {
            console.log(' Result', res.data)
            this.setState({data: res.data})
        })
  }

  renderPositionData() {
    let tableData = this.state.data;

    return (  
        <Table striped bordered condensed hover>
            <thead>
                <tr>
                    <th>Year</th>
                    <th>Position</th>
                </tr>
            </thead>
        <tbody>
            {
                tableData.map(function(o,i){
                    return (
                        <tr key={i+1}>
                            <td>{o.Season_Year}</td>
                            <td>{o.Pos}</td>
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
    console.log('bowler', gData, Object.keys(gData).length)
    return (
      <div className="team_results">
        <h3>Team Position Stats</h3>
        {this.renderPositionData()}
      </div>
    );
  }
}

export default TeamPosition;