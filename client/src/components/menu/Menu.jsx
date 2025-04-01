import Right from "./Right"
import Left from "./Left"
import { useState } from "react"



const Menu = ({searchVal, setSearchVal}) => {
    return(
        <div id="menu">
            <Left choice={searchVal}/>
            <Right onSearchChange={setSearchVal}/>
        </div>
    )
}

export default Menu