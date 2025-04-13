import React from "react";
import ChoiceCountry from './ChoiceCountry'     //Import the country choice
import NEW_SessionNum from './AISummary'        //Import the Session Number generated from AISummary
import api_conn from 'src/utils/api';

function Info(){
    return(
        <div id="info-box">
            <div className="title">
                <h1>Info</h1>
            </div>
            <div className="information">
                <p>
                Feature coming sprint 3.
                </p>
            </div>
        </div>
    )
}

export default Info;