import { useEffect, useState } from "react";

const PrecipitationKey = ({filter}) =>{
    //decides when to show the temperature key
    const [active,setActive] = useState(false);
    //prop is current filter
    useEffect(()=>{
        if(filter === "Precipitation"){
            setActive(true);
        } else {
            setActive(false);
        }
    },[filter])

    //if the current filter is "Temperature"

    return (
        <>
            {active && (
                <div className="precip-key-container">
                    <div className="text-container">
                        <h3>Precipitation</h3><p>(mmHg)</p>
                    </div>
                    
                    <div className="precip-key-gradient"></div>
                    <div>
                        <svg width="240" height="10">
                            <line 
                            x1="16" y1="10" x2="230" y2="10"
                            className="straight"
                            />
                        </svg>
                    </div>

                    <div>
                        <p>0.1</p>
                        <p>10</p>
                    </div>
                </div>
            )}
        </>
    )
}
export default PrecipitationKey;