import React, { useEffect, useState, useRef } from "react";
import ChoiceCountry from './ChoiceCountry'
import NEW_SessionNum from './AISummary'
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
        if (!choiceMade) return;

        // always show loading text first
        setContent(Warning_MSG);
        

        //Cancel the Previous request if one is currently active so we are sure only selected country is queried
        if(requestAbortRef.current){
            requestAbortRef.current.abort()
        }

        //Create a controller for the post request
        const controller = new AbortController();
        requestAbortRef.current = controller;


        // Increment id to only take the last one
        const requestId = ++requestIdRef.current;

        api_conn.post(
                "/api/Agent/",
                {
                    country: choiceMade,
                    FilterSelected: FilterName,
                    session: NEW_SessionNum,
                },
                {
                    headers: { "Content-Type": "application/json" },
                }
            )
            .then((response) => {
                if (requestId !== requestIdRef.current) return;

                setContent(response.data);
            })
            .catch((error) => {
                if (requestId !== requestIdRef.current) return;

                console.error("Error:", error);
                setContent("Error retrieving AI analysis.");
            });
    }, [choiceMade, FilterName]);

    // ================================
    // Typewriter Effect
    // ================================

    const [displayText, setDisplayText] = useState("");
    const [show, setShow] = useState(false);
    const [displayTitle, setDisplayTitle] = useState("AI");
    const [fade, setFade] = useState(false);
    const timeoutID = useRef(null);

    useEffect(() => {
        clearTimeout(timeoutID.current);

        if (choiceMade == null) setShow(false);
        else setShow(true);

        if (show) {
            setDisplayText("");
            let i = 0;
            const chars = Array.from(content);

            const tick = () => {
                if (i < chars.length - 1) {
                    if (i === 0) setDisplayText(chars[0]);
                    setDisplayText((prev) => prev + chars[i]);
                    i++;
                    timeoutID.current = setTimeout(tick, 10);
                }
            };

            tick();
        } else {
            setDisplayText("");
        }

        return () => clearTimeout(timeoutID.current);
    }, [choiceMade, show, content]);

    return (
        <div id="atlas-intel" className={choiceMade ? "active" : ""}>
            <div id="ai-title">
                <h1>{displayTitle}</h1>
            </div>

            <div className={show ? "atlas-response-container-anim" : "atlas-response-container"}>
                {content === Warning_MSG && displayText !== "" ? (
                    <Quantum size="100" speed="2.75" color="white" />
                ) : (
                    <ReactMarkdown>{displayText}</ReactMarkdown>
                )}
            </div>
        </div>
    );
}

export default AtlasIntel;

