import React from "react";
import ToggleMenu from "./ToggleMenu";
import Search from "./Search";
import AtlasIntel from './AtlasIntel';

const Right = ({choice, onSearchChange, onFilterSelection, activeFilter}) => {      //FilterName returns exact name of currently selected filter (will be null if no filter is selected)
    return(
        <div id="right">
            <Search onChangeHandle={onSearchChange}/>
            <ToggleMenu choiceMade={choice} onFilterSelection={onFilterSelection}/>
            <AtlasIntel choiceMade={choice} FilterName={activeFilter}/>            
        </div>
    )
}

export default Right;