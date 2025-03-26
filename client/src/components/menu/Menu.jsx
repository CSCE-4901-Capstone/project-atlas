import Right from "./Right"
import Left from "./Left"
import { useState } from "react"



function Menu() {
    //Variables from the top down
    const [searchVal,setSearchVal] = useState('');
    
    return(
        <div id="menu">
            <Left choice={searchVal}/>
            <Right onSearchChange={setSearchVal}/>
        </div>
    )
}

export default Menu