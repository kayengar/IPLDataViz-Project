import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import axios from 'axios';

const URLExt = 'season/teamslogruns/2008'

class SeasonSlogRuns extends Component {
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
      let slogruns = []
      let middleruns = []
      let powerruns = []
      let teamnames = []
      let year=[]
      res.forEach(function(val){
          slogruns.push(val['Slogruns'])
          middleruns.push(val['Middleruns'])
          powerruns.push(val['Powerruns'])
          teamnames.push(val['Team_Name'])
          year.push(val['Season_Year'])
      })
      let tmpArr = []
      tmpArr.push(slogruns)
      tmpArr.push(middleruns)
      tmpArr.push(powerruns)
      tmpArr.push(teamnames)
      tmpArr.push(year)
      return tmpArr
  }

  renderGraph() {
    let graphData = this.state.data;
    let result = this.parseGraphData(graphData);
    console.log('Hello',result[4])
    console.log('Hello',result[3])
    console.log('Hello',result[2])
    console.log('Hello',result[1])
    console.log('Hello',result[0])
    let config = {
      chart: {
            type: 'column'
        },
        title: {
            text: 'Teams vs Slog Runs for the year '+result[4][0]
        },
        subtitle: {
            text: 'Source: kaggle.com'
        },
        xAxis: {
            categories: result[3],
            title: {
                text: 'Team Names'
            }
        },
        yAxis: {
            title: {
                min : 0,
                text: 'Slog Runs'
            }
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0,
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: true
            }
        },
        series: [{
            name: 'Powerplay Runs of the year'+result[4][0],
            data: result[2]
        },
        {
            name: 'Middle Runs of the year'+result[4][0],
            data: result[1]
        },
        {
            name: 'Slog Runs of the year'+result[4][0],
            data: result[0]
        }]
        
    }
    return(<ReactHighcharts config={config} ref='chart'></ReactHighcharts>)
  }

  componentWillUnmount() {
    this.refs.chart.destroy;
  }

  render() {
    let gData = this.state.data
    console.log('In season test', gData, Object.keys(gData).length)
    return (
      <div className="season_slogruns">
        {this.renderGraph()}
      </div>
    );
  }
}

export default SeasonSlogRuns;