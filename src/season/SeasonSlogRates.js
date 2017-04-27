import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import axios from 'axios';

const URLExt = 'season/teamslogrunrates'

class SeasonSlogRates extends Component {
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
      axios.get(`${this.props.urlExt}/${url}/${this.props.currentYr}`)
        .then(res => {
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
    let config = {
        chart: {
            type: 'column',
            options3d: {
            enabled: true,
            alpha: 15,
            beta: 15,
            depth: 50,
            viewDistance: 25
        },
        width: 600,
        height:400
        },
        title: {
            text: 'Teams vs Slog Run,Economy Rates in year- '+result[2][0]
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
            name: 'Slog Run Rate for the year'+result[2][0],
            data: result[3]
        },
        {
            name: 'Slog Economy Rate for the year'+result[2][0],
            data: result[0]
        }
        ]
    }
        return(<ReactHighcharts config={config} ref='chart'></ReactHighcharts>)
  }

  componentWillUnmount() {
    this.refs.chart.destroy;
  }

  render() {
    let gData = this.state.data
    console.log('In season', gData, Object.keys(gData).length)
    return (
      <div className="season_slogrates">
        {this.renderGraph()}
      </div>
    );
  }
}

export default SeasonSlogRates;