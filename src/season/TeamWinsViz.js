import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import axios from 'axios';

const URLExt = 'season/teamwins'

class TeamWinsViz extends Component {
  constructor(props) {
      super(props);
      this.state = {
          data: []
      }
      this.loadGraphData = this.loadGraphData.bind(this);
  }

  shouldComponentUpdate(nextProps, nextState) {
      return this.props.currentYr !== nextProps.currentYr || this.state.data !== nextState.data
  }

  componentDidMount() {
      this.loadGraphData(URLExt);
  }

  loadGraphData(url) {
      axios.get(`${this.props.urlExt}/${url}/${this.props.currentYr}`)
        .then(res => {
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
    let config = {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Teams vs No. of Wins for the year '+ this.props.currentYr
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
      <div className="season_wins">
        {(Object.keys(gData).length) ? this.renderGraph(): null}
      </div>
    );
  }
}

export default TeamWinsViz;