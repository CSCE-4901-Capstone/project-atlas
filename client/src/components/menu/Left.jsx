import React from "react";
import Logo from './Logo'
import AISummary from "./AISummary";
import Help from "./Help";

function Left() {
    return(
        <div id="left">
            <div id='logo'>
                <Logo/>
            </div>
            <div id='AI'>
                <AISummary/> 
            </div>
            <div id="help">
                <Help/>
            </div>
        </div>
    )
}

export default Left;
