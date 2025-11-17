import React, { useEffect, useState, useRef } from "react";
import ChoiceCountry from './ChoiceCountry'     //Import the country choice
import NEW_SessionNum from './AISummary'        //Import the Session Number generated from AISummary
import api_conn from 'src/utils/api';
import { Quantum } from 'ldrs/react';
import 'ldrs/react/Quantum.css'
import ReactMarkdown from 'react-markdown'

//This is where Atlas Intelligence will export its summary from the agent.

function AtlasIntel({choiceMade,FilterName}){                   //FilterName is the name of the filter being currently selected
    //Dummy AI agent response string set to dummy data for printing the response **REMOVE THIS OR SET IT TO THE RESPONSE WHEN CONTENT IS DELIVERED**
    const Warning_MSG = "Loading Agent response...\nAs weather, flight, and news data is being considered in the holistic analysis, please be aware that the processing time can take up to approximately 1 minute"

    console.log("AtlasIntel rendered, choiceMade =", choiceMade);
    
    //set content is the text displayed. Just do setContent = response (No need for UseEffect)
    const [content,setContent] = useState(Warning_MSG);
    
    //variable used to keep track of currently active post requests so they can be cancelled if needed
    const requestAbortRef = useRef(null);


    //Get the analysis data from the backend
    useEffect(() => {
        console.log("AtlasIntel rendered, choiceMade =", choiceMade);
        if (!choiceMade) return;   //don’t send null

        //reset warning between every click
        setContent(Warning_MSG);
        

        //Cancel the Previous request if one is currently active so we are sure only selected country is queried
        if(requestAbortRef.current){
            requestAbortRef.current.abort()
        }

        //Create a controller for the post request
        const controller = new AbortController();
        requestAbortRef.current = controller;


        api_conn.post("/api/Agent/",{               //HERE ADD A VARIABLE TO RETRIVE THE ACTIVE FILTER NAME {FilterName} variable!!!!
            country: choiceMade,
            FilterSelected: FilterName,
            session: NEW_SessionNum,},//"session123"
            {
            headers : {"Content-Type": "application/json"},
            signal: controller.signal                       //Pass an abort signal every post request to prevent queing post requests
            },
        )
        .then((response) =>{
            console.log("response FROM views.py:", response.data);
            setContent(response.data);
        })
        .catch((error) => {

            if(error?.name === "AbortError" || error?.code === "ERR_CANCELED"){
                console.log("Previous POST request for Agent cancelled.");
                return;
            }

            console.error("Error:", error);      //catch error and display if encountered
        });          
    
        //ensure that that the request is cancelled upon selection of another country
        return() => {
            if(requestAbortRef.current){
                requestAbortRef.current.abort();
            }
        };
    
    },[choiceMade,FilterName]);        //ADD FilterName only AI has been fully optimized
    




    //DisplayText useStates
    const [displayText,setDisplayText] = useState("");
    const [show,setShow] = useState(false);
    //Title Fade into expand useStates
    const [displayTitle,setDisplayTitle] = useState("AI");
    const [fade,setFade] = useState(false);
    //Necessary timeoutID useRef variable for precision timeout clearing 
    const timeoutID = useRef(null);


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
    },[choiceMade,show,content])

    return(
        <div 
        id="atlas-intel"
        className={choiceMade ? "active" : ""}
        >
            <div
            id="ai-title" 
            >
                <h1>{displayTitle}</h1>
            </div>
            <div 
            className={show ? "atlas-response-container-anim" : "atlas-response-container"}
            >
                {
                    content == Warning_MSG && displayText != "" ?
                    <Quantum
                    size="100"
                    speed="2.75"
                    color="white"
                    /> : 
                    <ReactMarkdown>
                        {displayText}
                    </ReactMarkdown>
                            
                }

            </div>
        </div>
    )
}

export default AtlasIntel;