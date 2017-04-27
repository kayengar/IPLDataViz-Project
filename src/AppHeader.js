import React, { Component } from 'react';
import logo from './Cricketball.png';
import './App.css';
import 'animate.css';

class AppHeader extends Component {
  render() {
    return (
        <div className="App-header">
          <img src={logo} className={["App-logo", "animated"].join(' ')} alt="logo" />
          <h2>Indian Premier League Analytics</h2>
        </div>
    );
  }
}

export default AppHeader;
