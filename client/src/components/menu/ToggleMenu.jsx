import { useEffect, useState } from "react";
import '../../styles/Atlas.css'

function toggleMenu() {
    return(
        <div id="toggle-menu">
            <div className="title">
                <h1>Filters</h1>
            </div>
                <div id="toggle-radio-group">
                    <label className="custom-label">
                        <input
                            type="radio"
                            id="Topography"
                            name='toggles'
                        />
                        <span className="custom-radio"></span>Topography
                    </label>
                    <label className="custom-label">
                        <input
                            type="radio"
                            id="Borders"
                            name='toggles'
                        />
                        <span className="custom-radio"></span>Borders
                    </label>
                    <label className="custom-label">
                        <input
                            type="radio"
                            id="Flights"
                            name='toggles'
                        />
                        <span className="custom-radio"></span>Flights
                    </label>

                </div>
        </div>

    )
}

export default toggleMenu;