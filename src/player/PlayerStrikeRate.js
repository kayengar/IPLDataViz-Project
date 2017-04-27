import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import axios from 'axios'; 

const URLExt = 'strikerate'

class PlayerStrikeRate extends Component {
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
      axios.get(`${this.props.urlExt}/${url}/${this.props.pId}`)
        .then(res => {
            this.setState({data: res.data})
        })
  }

  parseGraphData(res) {
      let strikerate = []
      let overs = []
      let names = []
      res.forEach(function(val){
          strikerate.push(val['Batsman_Scored'])
          overs.push(val['Over_Id'])
          names.push(val['Player_Name'])
      })
      let tmpArr = []
      tmpArr.push(strikerate)
      tmpArr.push(overs)
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
        text: 'Striker Rate in 20 overs-'+result[2][0]
    },
    subtitle: {
        text: 'Source: Kaggle.com'
    },
    xAxis: {
        categories: result[1],
        crosshair: true
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Strike Rate'
        }
    },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        }
    },
    series: [{
        name: 'Strike Rate',
        data: result[0]
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
      <div className="player_strikerate">
        {this.renderGraph()}
      </div>
    );
  }
}

export default PlayerStrikeRate;
