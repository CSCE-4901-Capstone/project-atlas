import React from "react";
//import Logo from './Logo'
import AISummary from "./AISummary";
import Help from "./Help";

const Left = ({choice}) => {
    return(
        <div id="left">
            <div id='AI'>
                <AISummary chCountry={choice}/> 
            </div>
            <div id="help">
                <Help/>
            </div>

        </div>
    )
}

export default Left;
