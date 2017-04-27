import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import axios from 'axios'; 

const perfSplineData = 'performance'

class TeamPerformance extends Component {
  constructor(props) {
      super(props);
      this.state = {
          data: []
      }
      this.loadGraphData = this.loadGraphData.bind(this);
  }

  componentWillMount() {
      this.loadGraphData();
  }

  loadGraphData(url) {
      let {teamid, seasonYear} = this.props
      axios.get(`${this.props.urlExt}/${perfSplineData}/${teamid}/${seasonYear}`)
        .then(res => {
            this.setState({data: res.data})
        })
  }

  parseGraphData(res) {
      let overs = []
      let runrates = []
      let econrates = []
      res.forEach(function(val){
          overs.push(val['Over_Id'])
          runrates.push(val['Run_Rate'])
          econrates.push(val['Econ_Rate'])
      })
      let tmpArr = []
      tmpArr.push(overs)
      tmpArr.push(runrates)
      tmpArr.push(econrates)
      return tmpArr
  }

  renderGraph() {
    let graphData = this.state.data;
    let result = this.parseGraphData(graphData);
    console.log('Over',result[0])
    let config = {
     chart: {
            type: 'spline'
        },
        title: {
            text: 'Overs vs Average Run Rate,Economy Rate'
        },
        subtitle: {
            text: 'Source: kaggle.com'
        },
        xAxis: {
            categories: result[0],
            title: {
                text: 'Over'
            }
        },
        yAxis: {
            title: {
                min : 0,
                text: 'Average Run Rate,Economy Rate'
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
            name: 'Average Run Rate',
            data: result[1]
        },
        {
            name: 'Average Economy Rate',
            data: result[2]
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
    this.refs.chart.destroy;
  }

  render() {
    let gData = this.state.data
    console.log('bowler', gData, Object.keys(gData).length)
    return (
      <div className="team_battingperformance">
        {(Object.keys(gData).length) ? this.renderGraph(): null}
      </div>
    );
  }
}

export default TeamPerformance;