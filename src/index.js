import React from 'react';
import ReactDOM from 'react-dom';
import {Router, Route, browserHistory} from 'react-router';
import App from './App';
import TeamView from './TeamView'
import './index.css';

ReactDOM.render(
  <Router history={browserHistory}>
      <Route path='/' component={App}/>
      <Route path='/teamPage' component={TeamView}/>
      {/*<Route path='/seasons' component={SeasonView}></Route>*/}
  </Router>,
  document.getElementById('root')
);
