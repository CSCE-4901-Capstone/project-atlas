import React from "react";
import Logo from './Logo'
import AISummary from "./AISummary";
import Help from "./Help";

const Left = ({choice}) => {
    return(
        <div id="left">
            <div id='logo'>
                <Logo/>
            </div>
            <div id='AI'>
                <AISummary chCountry={choice}/> 
            </div>
            {/* Commented out for demo purposes. Also not reflected on the design document
                <div id="help">
                    <Help/>
                </div>        
            */}

        </div>
    )
}

export default Left;
