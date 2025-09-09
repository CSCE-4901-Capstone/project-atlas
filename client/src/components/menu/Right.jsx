import React from "react";
import ToggleMenu from "./ToggleMenu";
import Search from "./Search";
import AtlasIntel from './AtlasIntel';

const Right = ({onSearchChange, onFilterSelection}) => {
    return(
        <div id="right">
            <Search onChangeHandle={onSearchChange}/>
            <ToggleMenu onFilterSelection={onFilterSelection}/>
            <AtlasIntel/>
        </div>
    )
}
export default Right;
