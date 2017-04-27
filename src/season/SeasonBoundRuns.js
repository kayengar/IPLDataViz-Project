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

  shouldComponentUpdate(nextProps, nextState) {
      return this.props.currentYr !== nextProps.currentYr || this.state.data !== nextState.data
  }

//   componentWillMount() {
//     this.loadGraphData(URLExt);
//   }

  componentDidMount() {
    this.loadGraphData(URLExt);
  }

  loadGraphData(url) {
      console.log(`${this.props.urlExt}/${url}/${this.props.currentYr}`)
      axios.get(`${this.props.urlExt}/${url}/${this.props.currentYr}`)
        .then(res => {
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
    console.log('Result', result)
    let config = {
        chart: {
        type: 'bar'
    },
    title: {
        text: 'Boundary Runs in Season-'+this.props.currentYr
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
    console.log('SeasonBound', this.props.currentYr)
    return (
      <div className="season_boundruns">
         {this.renderGraph()}
      </div>
    );
  }
}

export default SeasonBoundRuns;
