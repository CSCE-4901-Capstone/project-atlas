import React from "react";
import ToggleMenu from "./ToggleMenu";
import Search from "./Search";
import Info from './Info';

const Right = ({onSearchChange, onFilterSelection, activeFilter}) => {
    return(
        <div id="right">
            <Search onChangeHandle={onSearchChange}/>
            <ToggleMenu 
              onFilterSelection={onFilterSelection} 
              activeFilter={activeFilter}
            />
            <Info/>
        </div>
    )
}

export default Right;