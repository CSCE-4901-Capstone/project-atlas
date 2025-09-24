import Right from "./Right"
import Left from "./Left"

const Menu = ({searchVal, setSearchVal, onFilterSelection, activeFilter}) => {
    return(
        <div id="menu">
            <Left choice={searchVal}/>
            <Right choice={searchVal} onSearchChange={setSearchVal} onFilterSelection={onFilterSelection} activeFilter={activeFilter}/>
        </div>
    )
}

export default Menu;