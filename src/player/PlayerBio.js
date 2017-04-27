import React, { Component } from 'react';

class PlayerBio extends Component {
  render() {
        let {Player_Name, Batting_Style, Bowling_Style, Country, Dismissals, Wickets, Batsman_Scored} = this.props.playerDetails
        return(
            <div className="container">
                <div className="row">
                    <div className="col-md-offset-5 col-md-10 col-lg-offset-5 col-lg-8">
                    <div className="well profile">
                        <div className="col-sm-12">
                            <div className="col-xs-12 col-sm-12">
                                <h2>{Player_Name}</h2>
                                <p><strong>Runs Scored: </strong> {Batsman_Scored} </p>                                
                                <p><strong>Batting Style: </strong> {(Batting_Style) ? Batting_Style.replace('_',' ') : Batting_Style} </p>
                                <p><strong>Bowling Style: </strong> {Bowling_Style} </p>
                                <p><strong>Country: </strong> {Country} </p>
                                <p><strong>Dismissals: </strong> {Dismissals} </p>
                                <p><strong>Wickets: </strong> {Wickets} </p>
                            </div>
                        </div>            
                    </div>                 
                    </div>
                </div>
            </div>
        )
  }
}

export default PlayerBio;