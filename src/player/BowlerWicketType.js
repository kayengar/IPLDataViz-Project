import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import axios from 'axios'; 

const URLExt = 'player/playerwickettype'

class BowlerWicketType extends Component {
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
      let dismissaltype = []
      let wickets = []
      let names = []
      res.forEach(function(val){
          dismissaltype.push(val['Dismissal_Type'])
          wickets.push(val['Wickets'])
          names.push(val['Player_Name'])
      })
      let tmpArr = []
      tmpArr.push(dismissaltype)
      tmpArr.push(wickets)
      tmpArr.push(names)
      return tmpArr
  }

  renderGraph() {
    let graphData = this.state.data;
    let result = this.parseGraphData(graphData);
    console.log('kannan',result[0])
    let config = {
        chart: {
        type: 'column'
    },
    title: {
        text: 'Classification of Wickets-'+result[2][0]
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
      <div className="bowler_wickettype">
        {(Object.keys(gData).length) ? this.renderGraph(): null}
      </div>
    );
  }
}

export default BowlerWicketType;
