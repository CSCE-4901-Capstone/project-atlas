import { useEffect, useState } from "react";

const TemperatureKey = ({filter}) =>{
    //decides when to show the temperature key
    const [active,setActive] = useState(false);
    //prop is current filter
    useEffect(()=>{
        if(filter === "Temperature"){
            setActive(true);
        } else {
            setActive(false);
        }
    },[filter])

    //if the current filter is "Temperature"

    return (
        <>
            {active && (
                <div className="temp-key-container">
                    <div className="temp-key-gradient"></div>
                    <div>
                        <svg width="240" height="10">
                            <line 
                            x1="16" y1="10" x2="230" y2="10"
                            className="straight"
                            />
                        </svg>
                    </div>

                    <div>
                        <p>-50C</p>
                        <p>40C</p>
                    </div>
                </div>
            )}
        </>
    )
}
export default TemperatureKey