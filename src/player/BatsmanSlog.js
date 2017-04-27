import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import axios from 'axios'; 

const URLExt = 'player/batsmanslogovers/32'

class BatsmanSlog extends Component {
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
      
      let runs = []
      let overs = []
      res.forEach(function(val){
          runs.push(val['Batsman_Scored'])
          overs.push(val['Over_Id'])
      })
      let tmpArr = []
      tmpArr.push(runs)
      tmpArr.push(overs)
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
        type: 'pie'
    },
    title: {
        text: 'Slog over Runs classification'
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
        name: 'Slog over Runs',
        colorByPoint: true,
        data: [{
            name:'Over 15',
            y: result[0][0]
        }, {
            name:'Over 16',
            y: result[0][1]
        },
        {
            name:'Over 17',
            y: result[0][2]
        },
        {
            name:'Over 18',
            y: result[0][3]
        },
        {
            name:'Over 19',
            y: result[0][4]
        },
        {
            name:'Over 20',
            y: result[0][5]
        }
        ]
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
      <div className="batsman_slog">
        {(Object.keys(gData).length) ? this.renderGraph(): null}
      </div>
    );
  }
}

export default BatsmanSlog;