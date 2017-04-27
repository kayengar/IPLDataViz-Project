import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import axios from 'axios';

const URLExt = 'season/teamrunrates/2009'

class SeasonRates extends Component {
  constructor(props) {
      super(props);
      this.state = {
          data: []
      }
      this.loadGraphData = this.loadGraphData.bind(this);
  }

  componentWillMount() {
      this.loadGraphData(URLExt);
      console.log('in')
  }

  loadGraphData(url) {
      axios.get(`${this.props.urlExt}/${url}`)
        .then(res => {
            console.log(res.data)
            this.setState({data: res.data})
        })
  }

  parseGraphData(res) {
      let economyrates = []
      let teamNames = []
      let seasonyear = []
      let runrates =[]
      res.forEach(function(val){
          runrates.push(val['Run_Rate'])
          economyrates.push(val['Economy_Rate'])
          teamNames.push(val['Team_Name'])
          seasonyear.push(val['Season_Year'])
      })
      let tmpArr = []

      tmpArr.push(economyrates)
      tmpArr.push(teamNames)
      tmpArr.push(seasonyear)
      tmpArr.push(runrates)
      return tmpArr
  }

  renderGraph() {
    let graphData = this.state.data;
    let result = this.parseGraphData(graphData);
    console.log('Team names',result[1])
    console.log('hello from kannan')
    let config = {
        chart: {
            type: 'column',
            options3d: {
            enabled: true,
            alpha: 15,
            beta: 15,
            depth: 50,
            viewDistance: 25
        }
        },
        title: {
            text: 'Teams vs Run,Economy Rates in year-'+result[2][0]
        },
        subtitle: {
            text: 'Source: kaggle.com'
        },
        xAxis: {
            categories: result[1],
            title: {
                text: 'Team Names'
            }
        },
        yAxis: {
            title: {
                min : 0,
                text: 'Run,Economy Rate'
            }
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0,
                depth: 25,
                enableMouseTracking: true
            }
        },
         legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'top',
        x: -10,
        y: 50,
        floating: true,
        borderWidth: 1,
        shadow: true
    },
        series: [{
            name: 'Run Rate for the year'+result[2][0],
            data: result[3]
        },
        {
            name: 'Economy Rate for the year'+result[2][0],
            data: result[0]
        }
        ]
    }
    console.log(result)
    if(result[0].length) {   
        return(<ReactHighcharts config={config} ref='chart'></ReactHighcharts>)
    } else {
        return null
    }
  }

  componentWillUnmount() {
    this.refs.chart.destroy;
  }

  render() {
    let gData = this.state.data
    return (
      <div className="season_rates">
        {this.renderGraph()}
      </div>
    );
  }
}

export default SeasonRates;