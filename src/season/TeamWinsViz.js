import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import axios from 'axios';

const URLExt = 'season/teamwins/2008'

class TeamWinsViz extends Component {
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
      let noOfWins = []
      let teamNames = []
      let seasonyear = []
      res.forEach(function(val){
          noOfWins.push(val['Wins'])
          teamNames.push(val['Team_Name'])
          seasonyear.push(val['Season_Year'])
      })
      let tmpArr = []
      tmpArr.push(noOfWins)
      tmpArr.push(teamNames)
      tmpArr.push(seasonyear)
      return tmpArr
  }

  renderGraph() {
    let graphData = this.state.data;
    let result = this.parseGraphData(graphData);
    console.log('Team names',result[1])
    let config = {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Teams vs No. of Wins for the year '+result[2][0]
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
                text: 'Number of Wins'
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
            name: 'Wins for the year'+result[2][0],
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
    let gData = this.state.data
    console.log('In season', gData, Object.keys(gData).length)
    return (
      <div className="season_wins">
        {(Object.keys(gData).length) ? this.renderGraph(): null}
      </div>
    );
  }
}

export default TeamWinsViz;