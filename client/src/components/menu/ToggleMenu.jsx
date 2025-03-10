import { useEffect, useState } from "react";
import '../../styles/Atlas.css'
import ChoiceCountry from './ChoiceCountry'

function toggleMenu() {
    return(
        <>
            <div className="toggle-menu">
                <h1>Toggle Menu Here</h1>
            </div>
            <ChoiceCountry />
        </>

    )
}

export default toggleMenu;