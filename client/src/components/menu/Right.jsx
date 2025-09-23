import React from "react";
import ToggleMenu from "./ToggleMenu";
import Search from "./Search";
import AtlasIntel from './AtlasIntel';

const Right = ({choice, onSearchChange, onFilterSelection, activeFilter}) => {
    return(
        <div id="right">
            <Search onChangeHandle={onSearchChange}/>
            <ToggleMenu choiceMade={choice} onFilterSelection={onFilterSelection} activeFilter={activeFilter}/>
            <AtlasIntel/>
        </div>
    )
}

export default Right;