import { useEffect, useState } from "react";
import '../../styles/Atlas.css'

function toggleMenu() {
    return(
        <>
            <div id="toggle-menu">
            <h1>Filters</h1>
                <div id="toggle-radio-group">
                    <div>
                        <input
                            type="radio"
                            id="Topography"
                            name='toggles'
                        />
                        <label>Topography</label>
                    </div>
                    <div>
                        <input
                            type="radio"
                            id="Borders"
                            name='toggles'
                        />
                        <label>Borders</label>
                    </div>
                    <div>
                        <input
                            type="radio"
                            id="Flights"
                            name='toggles'
                        />
                        <label>Flights</label>
                    </div>

                </div>
            </div>
        </>

    )
}

export default toggleMenu;