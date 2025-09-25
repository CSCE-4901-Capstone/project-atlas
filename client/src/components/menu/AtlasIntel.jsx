import React, { useEffect, useState } from "react";
import ChoiceCountry from './ChoiceCountry'     //Import the country choice
import NEW_SessionNum from './AISummary'        //Import the Session Number generated from AISummary
import api_conn from 'src/utils/api';

//This is where Atlas Intelligence will export its summary from the agent.

function AtlasIntel({choiceMade}){
    const [active,setActive] = useState(false);


    //Apply expand animation when a country is selected
    useEffect(()=>{
        if(choiceMade != null){
            setActive(false);
        }
    },[])

    return(
        <div 
        id="atlas-intel"
        className={choiceMade ? "active" : ""}
        >
            <div className="atlas-title">
                <h1>AI</h1>
            </div>
            <div className="atlas-response-container">
                <p>
                    {/*This is where the AI response would be received */}
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                </p>
            </div>
        </div>
    )
}

export default AtlasIntel;