import {useEffect, useRef} from "react";


function WelcomeScreen({onClose}){
    const popupRef = useRef(null);

    useEffect(() => {
        function handleClick(e){
            console.log(popupRef.current)
            if(popupRef.current && !popupRef.current.contains(e.target)) {
                onClose();
            }
        }
        document.addEventListener("mousedown", handleClick);

        return () => {
            document.removeEventListener("mousedown", handleClick);
        }
    }, [onClose]);


    return(
        <div 
        ref={popupRef}
        className="welcome-container">
                <p>Welcome to Atlas Global</p>
        </div>
    )
}

export default WelcomeScreen;