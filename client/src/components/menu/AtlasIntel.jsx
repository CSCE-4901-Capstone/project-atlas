import React, { useEffect, useState, useRef } from "react";
import ChoiceCountry from './ChoiceCountry'     //Import the country choice
import NEW_SessionNum from './AISummary'        //Import the Session Number generated from AISummary
import api_conn from 'src/utils/api';

//This is where Atlas Intelligence will export its summary from the agent.

function AtlasIntel({choiceMade}){
    //Dummy AI agent response string set to dummy data for printing the response **REMOVE THIS OR SET IT TO THE RESPONSE WHEN CONTENT IS DELIVERED**
    console.log("AtlasIntel choiceMade:", choiceMade);
    //set content is the text displayed. Just do setContent = response (No need for UseEffect)
    const [content,setContent] = useState("Loading Agent response...");
    
    
    

    //Get the analysis data from the backend
    useEffect(() => {
        //if (!choiceMade) return;   //don’t send null

        api_conn.post("/api/Agent/",{
            country: choiceMade,
            session: NEW_SessionNum,},
            {
            headers : {"Content-Type": "application/json"},
            },
        )
        .then((response) =>{
            setContent(response.data);
        })
        .catch((error) => console.error("Error:", error));          //catch error and display if encountered
    },[ChoiceCountry,NEW_SessionNum]);
    
    //DisplayText useStates
    const [displayText,setDisplayText] = useState("");
    const [show,setShow] = useState(false);
    //Title Fade into expand useStates
    const [displayTitle,setDisplayTitle] = useState("AI");
    const [fade,setFade] = useState(false);
    //Necessary timeoutID useRef variable for precision timeout clearing 
    const timeoutID = useRef(null);

    // Title Fade in and out animation
    /*
    useEffect(() => {
        // start fade-out immediately
        setFade(true);

        // timeout slightly longer than CSS transition to ensure browser registers it
        const timeout = setTimeout(() => {
            // swap text after fade-out completes
            setDisplayTitle(show ? "Atlas Intelligence" : "AI");
            // trigger fade-in
            setFade(false);
        }, 600);

        // cleanup to prevent multiple timers
        return () => clearTimeout(timeout);
    }, [show]);
    */




    //Apply animation for Agent response when text is available
    useEffect(()=>{
        //Every useEffect check needs to clear the current timeoutID
        clearTimeout(timeoutID.current);

        //For the div animation. Adds an active class name for the parent div
        if(choiceMade == null){
            setShow(false);
        } else {
            setShow(true);
        }

        //Start title fade expand logic


        //End title fade expand logic

        //Check if show is true
        if(show){
            //reset display to a blank state ""
            setDisplayText("");
            //variables
            let i=0;
            const chars = Array.from(content);
            
            //Tick function is to have the text scroll onto the screen one character at a time 
            const tick = () =>{
                if(i<chars.length-1){
                    //Ensures that the first char is added to the displayed text
                    if(i ==  0){
                        setDisplayText(chars[0]);
                    }
                    setDisplayText((prev)=> prev + chars[i]);
                    i++;
                    timeoutID.current = setTimeout(tick, 10);
                }
            }
            //Start the function
            tick();
        } else {
            //else setDisplay to ""
            setDisplayText("");
        }
        //Always clear timeout buffers
        return () => {
            clearTimeout(timeoutID.current);
            //clearTimeout(titleTimeout)
        }
    },[choiceMade,show])

    return(
        <div 
        id="atlas-intel"
        className={choiceMade ? "active" : ""}
        >
            <div
            id="ai-title" 
            className={fade ? "ai-hide" : ""}
            >
                <h1>{displayTitle}</h1>
            </div>
            <div 
            className="atlas-response-container"
            >
                <p
                className={show ? "anim" : ""}
                >
                    {displayText}
                </p>
            </div>
        </div>
    )
}

export default AtlasIntel;