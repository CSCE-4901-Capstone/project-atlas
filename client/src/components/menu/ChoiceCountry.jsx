import { useState, useEffect } from "react";

function ChoiceCountry() {
    const [choice,setChoice] = useState('Earth');
    

    return(
        <div className="country-choice">
            <h1>{choice}</h1>
        </div>
    )
}

export default ChoiceCountry