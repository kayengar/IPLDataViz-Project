import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import {Reactbootstrap, Grid, Row, Col, Nav, NavItem} from 'react-bootstrap';
import './Runrateviz.css'
import axios from 'axios';
import configMap from './config.js';

const URLExt = 'season/teams'

class RunrateViz extends Component {
  constructor(props) {
      super(props);
      this.state = {
          teamList: [],
          defaultYear: 2008
  }
    this.handleSelect = this.handleSelect.bind(this);
    this.handleLogo = this.handleLogo.bind(this)
  }

  componentWillMount() {
    this.loadTeamList(this.state.defaultYear);
  }
  
  loadTeamList(seasonYr) {
      axios.get(`${this.props.urlExt}/${URLExt}/${seasonYr}`)
        .then(res => {
            console.log(res.data)
            this.setState({teamList: res.data})
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
      this.loadTeamList(e.target.text)
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
      return(
        <div>
            {
                teamLogos.map(function(o,i){
                    return(
                        <div className='teamLogos' key={o.Team_Id} onClick={this.handleLogo}>
                            <img src={require(`./images/Logos/${o.Team_Id}.png`)}/>
                        </div>
                    )
                })
            }
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
    console.log(result)
    if(result[0].length) {   
        console.log('render') 
        return(<ReactHighcharts config={config} ref='chart'></ReactHighcharts>)
    } else {
        return null
    }
  }

  componentWillUnmount() {
    this.refs.chart.destroy();
  }

  render() {
    return (
        <Grid>
            <Row className="show-grid">
                <Col xs={4} md={2}>
                    {this.seasonList()}
                </Col>
                <Col xs={14} md={10}>
                    {this.teamView()}
                </Col>
            </Row>
        </Grid>
    );
  }
}

export default RunrateViz;