import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import axios from 'axios'; 

const URLExt = 'season/teamboundruns'

class SeasonBoundRuns extends Component {
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
            console.log('bowlwe',res.data)
            this.setState({data: res.data})
        })
  }

  parseGraphData(res) {
      let totalruns = []
      let boundruns = []
      let names = []
      let seasons = []
      res.forEach(function(val){
          totalruns.push(val['Total_Runs'])
          boundruns.push(val['Bound_Runs'])
          names.push(val['Team_Name'])
          seasons.push(val['Season'])
      })
      let tmpArr = []
      tmpArr.push(totalruns)
      tmpArr.push(boundruns)
      tmpArr.push(names)
      tmpArr.push(seasons)
      return tmpArr
  }

  renderGraph() {
    let graphData = this.state.data;
    let result = this.parseGraphData(graphData);
    console.log('kannan',result[0])
    let config = {
        chart: {
        type: 'bar'
    },
    title: {
        text: 'Boundary Runs in Season-'+result[3][0]
    },
    xAxis: {
        categories: result[2]
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Runs'
        }
    },
    legend: {
        reversed: true
    },
    plotOptions: {
        series: {
            stacking: 'normal'
        }
    },
    series: [{
        name: 'Total Runs',
        data: result[0]
    }, {
        name: 'Boundary Runs',
        data: result[1]
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
      <div className="season_boundruns">
        {(Object.keys(gData).length) ? this.renderGraph(): null}
      </div>
    );
  }
}

export default SeasonBoundRuns;
