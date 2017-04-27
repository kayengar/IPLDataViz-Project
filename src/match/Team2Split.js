import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import axios from 'axios';

const URLExt = 'team2powerruns'

class Team2Split extends Component {
  constructor(props) {
      super(props);
      this.state = {
          data: []
      }
      this.loadGraphData = this.loadGraphData.bind(this);
  }

  componentWillMount() {
      this.loadGraphData(URLExt);
  }

  loadGraphData(url) {
      axios.get(`${this.props.urlExt}/${url}/${this.props.mId}`)
        .then(res => {
            this.setState({data: res.data})
        })
  }

  parseGraphData(res) {
      let powerruns = []
      let middleruns = []
      let slogruns = []
      let teamnames = []
      res.forEach(function(val){
          powerruns.push(val['Powerruns'])
          middleruns.push(val['Middleruns'])
          slogruns.push(val['Slogruns'])
          teamnames.push(val['Team_Name'])
      })
      let tmpArr = []
      tmpArr.push(powerruns)
      tmpArr.push(middleruns)
      tmpArr.push(slogruns)
      tmpArr.push(teamnames)
      return tmpArr
  }

  renderGraph() {
    let graphData = this.state.data;
    let result = this.parseGraphData(graphData);
    let config = {
        chart: {
        plotBackgroundColor: null,
        plotBorderWidth: 0,
        plotShadow: false
    },
    title: {
        text: 'Runs Scored-'+result[3][0],
        align: 'center',
        verticalAlign: 'middle',
        y: -110
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.y}</b>'
    },
    plotOptions: {
        pie: {
            dataLabels: {
                enabled: true,
                distance: -50,
                style: {
                    fontWeight: 'bold',
                    color: 'white'
                }
            },
            startAngle: -90,
            endAngle: 90,
            center: ['50%', '75%']
        }
    },
    series: [{
        type: 'pie',
        name: 'Runs',
        innerSize: '50%',
        data: [
            ['Powerplay',   result[0][0]],
            ['Middle',       result[1][0]],
            ['Slog', result[2][0]]
        ]
    }]

    }
        return(<ReactHighcharts config={config} ref='chart'></ReactHighcharts>)
  }

  componentWillUnmount() {
    this.refs.chart.destroy;
  }

  render() {
    let gData = this.state.data
    return (
      <div className="match_team2split">
        {this.renderGraph()}
      </div>
    );
  }
}

export default Team2Split;