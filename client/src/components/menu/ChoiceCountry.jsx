import { useState, useEffect } from "react";

const ChoiceCountry = ({choice}) => {
    const [displayed,setDisplayed] = useState(choice)
    console.log("Displayed: " + displayed)
    /*Works but the effect is delayed and looks off */
    const [fade, setFade] = useState(false);
    useEffect(()=>{
        if(choice == displayed){
            return;
        }
        setFade(true);

        const timeout = setTimeout(()=>{
            setDisplayed(choice);
            setFade(false);
        }, 600);
        return ()=>clearTimeout(timeout);
    }, [choice, displayed])

    return(
        <div 
        className="country-choice"
        >
            <h1
            className={fade ? "hide" : ""}
            >
                {displayed == null ? 'Earth' : displayed}
            </h1>
        </div>
    )
}

export default ChoiceCountry;
