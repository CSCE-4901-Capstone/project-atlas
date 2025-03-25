import React from "react";
import ToggleMenu from "./ToggleMenu";
import Search from "./Search";
import Info from './Info';

function Right() {
    return(
        <div id="right">
            <Search/>
            <ToggleMenu/>
            <Info/>
        </div>
    )
}
export default Right;