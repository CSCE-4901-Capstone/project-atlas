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
                A major fire at an electrical substation near London's Heathrow Airport caused a massive power outage today, 
                leading to the shutdown of the airport and impacting hundreds of thousands of passengers. At least 1,350 flights were affected, 
                including many from U.S. cities. 
                </p>
            </div>
        </div>
    )
}

export default Info;