import { useEffect, useState } from "react";
import '../../styles/Atlas.css'

//Create array of prefilled filters then render based on the length of the filter

// Have the toggle menu be built using an array of names
function ToggleMenu({ onFilterSelection }) {
    const [selected,setSelected] = useState(null);


  function handleFilterSelection(e) {
    const value = e.target.value;
    const newValue = selected === value ? null : value;
    setSelected(newValue);
    onFilterSelection(newValue);
  }

    return(
        <div id="toggle-menu">
            <div className="title">
                <h1>Filters</h1>
            </div>
                <div id="toggle-radio-group">
                    <label className="custom-label">
                        <input
                            type="checkbox"
                            value="Weather"
                            name='toggles'
                            checked={selected === "Weather"}
                            onChange={handleFilterSelection}
                        />
                        <span className="custom-radio"></span>Weather
                    </label>
                    <label className="custom-label">
                        <input
                            type="checkbox"
                            value="Flights"
                            name='toggles'
                            checked={selected === "Flights"}
                            onChange={handleFilterSelection}
                        />
                        <span className="custom-radio"></span>Flights
                    </label>
                </div>
        </div>

    )
}

export default ToggleMenu;
