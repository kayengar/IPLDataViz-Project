import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import axios from 'axios'; 

const URLExt = 'economyrate'

class PlayerEconRate extends Component {
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
            console.log('bowlwe',res.data)
            this.setState({data: res.data})
        })
  }

  parseGraphData(res) {
      let econrate = []
      let overs = []
      let names = []
      res.forEach(function(val){
          econrate.push(val['Economy_Rate'])
          overs.push(val['Over_Id'])
          names.push(val['Player_Name'])
      })
      let tmpArr = []
      tmpArr.push(econrate)
      tmpArr.push(overs)
      tmpArr.push(names)
      console.log('Wicket temp',tmpArr[1])
      return tmpArr
  }

  renderGraph() {
    let graphData = this.state.data;
    let result = this.parseGraphData(graphData)
    console.log('Name of the player',result[2][0])
    console.log('strikerate',result[0])
    console.log('names',result[1])
    let config = {
        chart: {
        type: 'line'
    },
    title: {
        text: 'EconomyRate in 20 overs-'+result[2][0]
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
            text: 'Economyrate'
        }
    },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        }
    },
    series: [{
        name: 'EconomyRate',
        data: result[0]
    } ]
    }
    console.log(result)
        return(<ReactHighcharts config={config} ref='chart'></ReactHighcharts>)

  }

  componentWillUnmount() {
    this.refs.chart.destroy;
  }

  render() {
    let gData = this.state.data
    console.log('bowler', gData, Object.keys(gData).length)
    return (
      <div className="player_econrate">
        {this.renderGraph()}
      </div>
    );
  }
}

export default PlayerEconRate;
