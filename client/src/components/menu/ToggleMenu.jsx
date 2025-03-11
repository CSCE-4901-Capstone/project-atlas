import { useEffect, useState } from "react";
import '../../styles/Atlas.css'
import ChoiceCountry from './ChoiceCountry'

function toggleMenu() {
    return(
        <>
            <div id="toggle-menu">
            <h1>Toggles</h1>
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
            <ChoiceCountry />
        </>

    )
}

export default toggleMenu;