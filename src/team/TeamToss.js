import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import axios from 'axios'; 

const URLExt = 'toss'

class TeamToss extends Component {
  constructor(props) {
      super(props);
      this.state = {
          data: []
      }
      this.loadGraphData = this.loadGraphData.bind(this);
  }

  componentWillMount() {
      this.loadGraphData();
      console.log('in')
  }

  loadGraphData() {
      let {teamid, seasonYear} = this.props
      axios.get(`${this.props.urlExt}/${URLExt}/${teamid}/${seasonYear}`)
        .then(res => {
            console.log('bowlwe',res.data)
            this.setState({data: res.data})
        })
  }

  parseGraphData(res) {
      let batwins = []
      let bowlwins = []
      res.forEach(function(val){
          batwins.push(val['BatWins'])
          bowlwins.push(val['BowlWins'])
      })
      let tmpArr = []
      tmpArr.push(batwins)
      tmpArr.push(bowlwins)
      return tmpArr
  }

  renderGraph() {
    let graphData = this.state.data;
    let result = this.parseGraphData(graphData);
    //console.log('kannan',result[0][0])
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
        text: 'Wins classification'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.y}</b>'
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
        name: 'Wins',
        colorByPoint: true,
        data: [{
            name:'Batting Wins',
            y: result[0][0]
        }, {
            name:'Bowling Wins',
            y: result[1][0]
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
    this.refs.chart.destroy();
  }

  render() {
    let gData = this.state.data
    console.log('bowler', gData, Object.keys(gData).length)
    return (
      <div className="team_teamtoss">
        {(Object.keys(gData).length) ? this.renderGraph(): null}
      </div>
    );
  }
}

export default TeamToss;