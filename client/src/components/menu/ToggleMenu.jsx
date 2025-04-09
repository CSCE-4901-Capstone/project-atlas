import { useEffect, useState } from "react";
import '../../styles/Atlas.css'

//Create array of prefilled filters then render based on the length of the filter

// Have the toggle menu be built using an array of names
function toggleMenu({ onFilterSelection }) {

  function handleFilterSelection(e) {
    onFilterSelection(e.target.value) 
  }

    return(
        <div id="toggle-menu">
            <div className="title">
                <h1>Filters</h1>
            </div>
                <div id="toggle-radio-group">
                    <label className="custom-label">
                        <input
                            type="radio"
                            value="Topography"
                            name='toggles'
                            onChange={handleFilterSelection}
                        />
                        <span className="custom-radio"></span>Topography
                    </label>
                    <label className="custom-label">
                        <input
                            type="radio"
                            value="Flights"
                            name='toggles'
                            onChange={handleFilterSelection}
                        />
                        <span className="custom-radio"></span>Flights
                    </label>

                </div>
        </div>

    )
}

export default toggleMenu;
