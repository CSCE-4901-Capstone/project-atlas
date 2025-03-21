import { useEffect, useState } from "react";
import '../../styles/Atlas.css'

function toggleMenu() {
    return(
        <div id="toggle-menu">
            <div className="title">
                <h1>Filters</h1>
            </div>
                <div id="toggle-radio-group">
                    <div>
                        <input
                            type="checkbox"
                            id="Topography"
                            name='toggles'
                        />
                        <label>Topography</label>
                    </div>
                    <div>
                        <input
                            type="checkbox"
                            id="Borders"
                            name='toggles'
                        />
                        <label>Borders</label>
                    </div>
                    <div>
                        <input
                            type="checkbox"
                            id="Flights"
                            name='toggles'
                        />
                        <label>Flights</label>
                    </div>

                </div>
        </div>

    )
}

export default toggleMenu;