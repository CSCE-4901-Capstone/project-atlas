import React, { useEffect, useState, useRef } from "react";
import ChoiceCountry from './ChoiceCountry'
import NEW_SessionNum from './AISummary'
import api_conn from 'src/utils/api';
import { Quantum } from 'ldrs/react';
import 'ldrs/react/Quantum.css'
import ReactMarkdown from 'react-markdown'

function AtlasIntel({choiceMade, FilterName}) {

    const Warning_MSG =
        "Loading Agent response...\nAs weather, flight, and news data is being considered in the holistic analysis, please be aware that the processing time can take up to approximately 1 minute";

    const [content, setContent] = useState(Warning_MSG);
    const requestIdRef = useRef(0)
    // ================================
    // FETCH AI SUMMARY
    // ================================
    useEffect(() => {
        if (!choiceMade) return;

        // always show loading text first
        setContent(Warning_MSG);

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
                    <div
                    style={{
                        height: "inherit",
                        width: "inherit",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center"
                    }}
                    >
                        <Quantum size="130" speed="2.75" color="white" />
                    </div>

                ) : (
                    <ReactMarkdown>{displayText}</ReactMarkdown>
                )}
            </div>
        </div>
    );
}

export default AtlasIntel;

