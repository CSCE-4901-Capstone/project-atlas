import { useState, useEffect } from "react";

const ChoiceCountry = ({choice}) => {
    return(
        <div className="country-choice">
            <h1>{choice == null ? 'Earth' : choice}</h1>
        </div>
    )
}

export default ChoiceCountry;
