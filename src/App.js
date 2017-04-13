import React, { Component } from 'react';
import logo from './Cricketball.png';
import './App.css';
import RunrateViz from './RunrateViz'
import SeasonView from './SeasonView'

const url = 'http://localhost:5000/iplviz'

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Indian Premier League Analytics</h2>
        </div>
        {/*<RunrateViz urlExt={url}/>*/}
        <SeasonView urlExt={url}/>
      </div>
    );
  }
}

export default App;
