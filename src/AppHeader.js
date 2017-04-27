import React, { Component } from 'react';
import logo from './Cricketball.png';
import './App.css';
import 'animate.css';
import {browserHistory} from 'react-router'

class AppHeader extends Component {
  constructor(props) {
    super(props)
    this.handleClick = this.handleClick.bind(this)
  }
  handleClick() {
    console.log('In')
    browserHistory.push('/mainPage')
  }

  render() {
    return (
        <div className="App-header">
          <img src={logo} className={["App-logo", "animated"].join(' ')} alt="logo" onClick={this.handleClick}/>
          <h2>Indian Premier League Analytics</h2>
        </div>
    );
  }
}

export default AppHeader;
