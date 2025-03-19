import React from "react";
import ToggleMenu from "./ToggleMenu";
import Search from "./Search";

function Right() {
    return(
        <div id="right">
            <Search/>
            <ToggleMenu/>
        </div>
    )
}
export default Right;