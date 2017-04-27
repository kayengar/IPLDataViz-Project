import React from 'react';
import ReactDOM from 'react-dom';
import {Router, Route, browserHistory} from 'react-router';
import App from './App';
import TeamView from './TeamView'
import PlayerDetails from './PlayerDetails'
import MatchDetails from './MatchDetails'
import './index.css';

ReactDOM.render(
  <Router history={browserHistory}>
      <Route path='/' component={App}/>
      <Route path='/mainPage' component={App}/>      
      <Route path='/teamPage' component={TeamView}/>
      <Route path='/playerDetails' component={PlayerDetails}/>
      <Route path='/matchDetails' component={MatchDetails}/>      
      {/*<Route path='/seasons' component={SeasonView}></Route>*/}
  </Router>,
  document.getElementById('root')
);
