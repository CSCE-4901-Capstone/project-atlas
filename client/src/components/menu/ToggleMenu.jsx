import { useEffect, useState } from "react";
import '../../styles/Atlas.css'

//**Array is global! Consider the data being passed from the server instead!**


// Have the toggle menu be built using an array of names
function ToggleMenu({ onFilterSelection }) {
    const [selected,setSelected] = useState(null);
    const filters = ["Flights", "Weather"];
    const [active, setActive] = useState(false);

  function handleFilterSelection(e) {
    const value = e.target.value;
    const newValue = selected === value ? null : value;
    setSelected(newValue);
    onFilterSelection(newValue);
  }
  //CSS expansion from filters
  

    return(
        <div 
        id="toggle-menu"
        className={`${active ? "active" : ""}`}
        onClick={() => setActive(!active)}
        >
            <div className="title">
                <h1>Filters</h1>
            </div>
            <div id="toggle-radio-group">
                {filters.map((filter) => (
                    <label 
                    key={filter} 
                    id="custom-label"
                    onClick={(e)=>e.stopPropagation()}
                    >
                    <input
                        type="checkbox"
                        value={filter}
                        name="toggles"
                        checked={selected === filter}
                        onChange={handleFilterSelection}
                    />
                    <span className="custom-radio"></span>{filter}
                    </label>
                ))}
            </div>

        </div>
    )
}

export default ToggleMenu;
