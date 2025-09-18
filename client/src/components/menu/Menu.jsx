import Right from "./Right"
import Left from "./Left"
import { useState } from "react"

const Menu = ({searchVal, setSearchVal, onFilterSelection}) => {
    return(
        <div id="menu">
            <Left choice={searchVal}/>
            <Right choice={searchVal} onSearchChange={setSearchVal} onFilterSelection={onFilterSelection}/>
        </div>
    )
}

export default Menu
