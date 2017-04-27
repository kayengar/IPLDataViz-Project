import React, { Component } from 'react';
import logo from './Cricketball.png';
import './App.css';
import 'animate.css';
import AppHeader from './AppHeader'
import SeasonView from "./SeasonView"

const url = '//localhost:5000/iplviz'

class App extends Component {
  render() {
    return (
      <div className="App">
        <AppHeader/>
        {/*<RunrateViz urlExt={url}/>*/}
        <SeasonView urlExt={url}/>
        {/*<PlayerView urlExt={url}/>*/}
      </div>
    );
  }
}

export default App;
