import React from "react";
//import Logo from './Logo'
import AISummary from "./AISummary";
import Help from "./Help";
import TemperatureKey from "./TemperatureKey";

const Left = ({choice, activeFilter}) => {
    return(
        <div id="left">
            <div 
            id='AI'
            className={ choice ? "active" : ""}
            >
                <AISummary chCountry={choice}/> 
            </div>
            <div id="Temp-Key">
                <TemperatureKey filter={activeFilter}/>
            </div>

        </div>
    )
}

export default Left;
