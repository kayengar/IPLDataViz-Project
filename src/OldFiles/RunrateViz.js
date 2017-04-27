import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import Reactbootstrap from 'react-bootstrap';
import './Runrateviz.css'
import axios from 'axios'; 

const URLExt = 'match'

class RunrateViz extends Component {
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
      axios.get(`${this.props.urlExt}/${url}`)
        .then(res => {
            this.setState({data: res.data})
        })
  }

  parseGraphData(res) {
      let innings1 = []
      let innings2 = []
     
      res['Innings1'].forEach(function(val){
          innings1.push(val.Runs)
      })
      res['Innings2'].forEach(function(val){
          innings2.push(val.Runs)
      })
      let tmpArr = []
      tmpArr.push(innings1)
      tmpArr.push(innings2)
      return tmpArr
  }

  renderGraph() {
    let graphData = this.state.data;
    let team1 = graphData['Team_One']
    let team2 = graphData['Team_Two']
    let xAxisScale = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
    let result = this.parseGraphData(graphData);
    let config = {
        chart: {
            type: 'line'
        },
        title: {
            text: 'Overall Runs Scored per Over'
        },
        subtitle: {
            text: 'Source: kaggle.com'
        },
        xAxis: {
            categories: xAxisScale,
            title: {
                text: 'Over'
            }
        },
        yAxis: {
            title: {
                text: 'Runs Scored'
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: true
            }
        },
        series: [{
            name: team2,
            data: result[1]
        }, {
            name: team1,
            data: result[0]
        }]
    }
        return(<ReactHighcharts config={config} ref='chart'></ReactHighcharts>)
  }

  componentWillUnmount() {
    this.refs.chart.destroy;
  }

  render() {
    let gData = this.state.data
    let team1 = gData['Team_One']
    let team2 = gData['Team_Two']
    let graphBanner = team2 + ' vs ' + team1
    return (
      <div className="runrate_innings">
        <div className="dropdown">
            <button className="btn btn-default dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
                KXIP vs CSK
                <span className="caret"></span>
            </button>
            <ul className="dropdown-menu" aria-labelledby="dropdownMenu1">
                <li><a href="#">KXIP vs CSK</a></li>
                <li><a href="#">Another action</a></li>
                <li><a href="#">Something else here</a></li>
            </ul>
        </div>
        <div>
            <h2>{graphBanner}</h2>
            {this.renderGraph()}
        </div>
      </div>
    );
  }
}

export default RunrateViz;