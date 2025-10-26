import React from "react";
//import Logo from './Logo'
import AISummary from "./AISummary";
import TemperatureKey from "./TemperatureKey";
import PrecipitationKey from "./PrecipitationKey"
import DisasterKey from "./DisasterKey";

const Left = ({choice, activeFilter}) => {
    let retFilter = null;
    console.log(activeFilter)
    switch(activeFilter){
        case "Temperature":
            retFilter = <TemperatureKey filter={activeFilter}/>;
            break;
        case "Precipitation":
            //Change to new filter key for precipitation when made
            retFilter = <PrecipitationKey filter={activeFilter}/>;
            break;
        case "Disasters":
            retFilter = <DisasterKey filter={activeFilter}/>
            break;
        default:
            retFilter = null;
    }
    console.log(retFilter)
    return(
        <div id="left">
            <div 
            id='AI'
            className={ choice ? "active" : ""}
            >
                <AISummary chCountry={choice}/> 
            </div>
            <div id="filter-Key">
                {retFilter}
            </div>

        </div>
    )
}

export default Left;
