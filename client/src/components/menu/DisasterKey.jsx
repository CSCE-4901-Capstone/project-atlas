import { useEffect, useState } from "react";
import drought from "../../assets/drought.png"
import ice from "../../assets/ice.png"
import volcano from "../../assets/volcano.png"
import wildfire from "../../assets/wildfire.png"

const DisasterKey = ({filter}) =>{
    //decides when to show the temperature key
    const [active,setActive] = useState(false);
    //prop is current filter
    useEffect(()=>{
        if(filter === "Disasters"){
            setActive(true);
        } else {
            setActive(false);
        }
    },[filter])

    console.log(filter)

    return (
        <>
            {active && (
                <div className="disaster-key-container">
                    <div className="disaster-container">
                        {/*Volcano*/}
                        <img src={volcano} alt="volcano image" />
                        <p>Volcanoes</p>
                    </div>
                    <div className="disaster-container">
                        {/*Wildfire*/}
                        <img src={wildfire} alt="wildfire image" />
                        <p>Wildfires</p>
                    </div>
                    <div className="disaster-container">
                        {/*Drought*/}
                        <img src={drought} alt="drought image" />
                        <p>Droughts</p>
                    </div>
                    <div className="disaster-container">
                        {/*Ice*/}
                        <img src={ice} alt="ice image" />
                        <p>Droughts</p>
                    </div>
                </div>
            )}
        </>
    )
}
export default DisasterKey;