import React from "react";
import ChoiceCountry from './ChoiceCountry'     //Import the country choice
import NEW_SessionNum from './AISummary'        //Import the Session Number generated from AISummary
import api_conn from 'src/utils/api';

//This is where Atlas Intelligence will export its summary from the agent.

function AtlasIntel(){
    return(
        <div id="atlas-intel">
            <h1>AI</h1>
        </div>
    )
}

export default AtlasIntel;