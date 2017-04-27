import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import axios from 'axios'; 

const URLExt = 'playerwicket'

class BowlerWickets extends Component {
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

  componentWillReceiveProps(nextProps) {
      this.setState({playerId: nextProps.playerId})
  }

  loadGraphData(url) {
      axios.get(`${this.props.urlExt}/${url}/${this.props.pId}`)
        .then(res => {
            this.setState({data: res.data})
        })
  }

  parseGraphData(res) {
      let years = []
      let wickets = []
      let names = []
      res.forEach(function(val){
          years.push(val['Season_Year'])
          wickets.push(val['Wickets'])
          names.push(val['Player_Name'])
      })
      let tmpArr = []
      tmpArr.push(years)
      tmpArr.push(wickets)
      tmpArr.push(names)
      return tmpArr
  }

  renderGraph() {
    let graphData = this.state.data;
    let result = this.parseGraphData(graphData)

    let config = {
        chart: {
        type: 'line'
    },
    title: {
        text: 'Number of Wickets-Seasonwise-'+result[2][0]
    },
    subtitle: {
        text: 'Source: Kaggle.com'
    },
    xAxis: {
        categories: result[0],
        crosshair: true
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Number of Wickets'
        }
    },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        }
    },
    series: [{
        name: 'Wickets',
        data: result[1]
    } ]
    }
        return(<ReactHighcharts config={config} ref='chart'></ReactHighcharts>)

  }

  componentWillUnmount() {
    this.refs.chart.destroy;
  }

  render() {
    let gData = this.state.data
    return (
      <div className="bowler_wickets">
        {this.renderGraph()}
      </div>
    );
  }
}

export default BowlerWickets;
