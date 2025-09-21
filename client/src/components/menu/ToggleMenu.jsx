import { useEffect, useState } from "react";
import '../../styles/Atlas.css'

// Have the toggle menu be built using an array of names
function ToggleMenu({ choiceMade, onFilterSelection }) {
    const [selected,setSelected] = useState(null);
    const filters = ["Flights", "Weather"];
    const [active, setActive] = useState(false);

  function handleFilterSelection(e) {
    const value = e.target.value;
    const newValue = activeFilter === value ? null : value;
    onFilterSelection(newValue);
  }
  useEffect(()=>{
    if(choiceMade != null){
        setActive(false);
    }
  }, [choiceMade])
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
