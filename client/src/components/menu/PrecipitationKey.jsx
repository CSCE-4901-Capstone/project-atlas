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
                    <div className="color-container">
                        {/*Snow - white */}
                        <div className="snow-color"></div>
                        <p>Snow</p>
                    </div>
                    <div className="color-container">
                        {/*Rain - Blue */}
                        <div className="rain-color"></div>
                        <p>Rain</p>
                    </div>
                    <div className="color-container">
                        {/*Storms - Orange*/}
                        <div className="storm-color"></div>
                        <p>Storm</p>
                    </div>
                </div>
            )}
        </>
    )
}
export default PrecipitationKey;