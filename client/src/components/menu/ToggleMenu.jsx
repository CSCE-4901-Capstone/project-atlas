import { useEffect, useState } from "react";
import '../../styles/Atlas.css'

function ToggleMenu({ onFilterSelection, activeFilter }) {

  function handleFilterSelection(e) {
    const value = e.target.value;
    const newValue = activeFilter === value ? null : value;
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
                            checked={activeFilter === "Weather"} //Check if weather toggle is active
                            onChange={handleFilterSelection}
                        />
                        <span className="custom-radio"></span>Weather
                    </label>
                    <label className="custom-label">
                        <input
                            type="checkbox"
                            value="Flights"
                            name='toggles'
                            checked={activeFilter === "Flights"}
                            onChange={handleFilterSelection}
                        />
                        <span className="custom-radio"></span>Flights
                    </label>
                </div>
        </div>

    )
}

export default ToggleMenu;
