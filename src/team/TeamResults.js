import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import axios from 'axios'; 

const URLExt = 'numberofwinlossnoresult'

class TeamResults extends Component {
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
      axios.get(`${this.props.urlExt}/${URLExt}/${teamid}/${seasonYear}`)
        .then(res => {
            console.log('teamresults',res.data)
            this.setState({data: res.data})
        })
  }

  parseGraphData(res) {
      let wins = []
      let loss = []
      let noresults = []
      res.forEach(function(val){
          wins.push(val['Wins'])
          loss.push(val['Loss'])
          noresults.push(val['No_Result'])
      })
      let tmpArr = []
      tmpArr.push(wins)
      tmpArr.push(loss)
      tmpArr.push(noresults)
      return tmpArr
  }

  renderGraph() {
    let graphData = this.state.data;
    let result = this.parseGraphData(graphData);
    let config = {
      chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie',
        width: 550,
        height: 350
    },
    title: {
        text: 'Wins,Loss,No Result'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.y}',
                style: {
                    color: 'black'
                }
            }
        }
    },
    series: [{
        name: 'Result',
        colorByPoint: true,
        data: [{
            name: 'Wins',
            y: result[0][0]
        }, {
            name: 'Loss',
            y: result[1][0]
        }, {
            name: 'No result',
            y: result[2][0]
        }]
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
      <div className="team_results">
        {(Object.keys(gData).length) ? this.renderGraph(): null}
      </div>
    );
  }
}

export default TeamResults;