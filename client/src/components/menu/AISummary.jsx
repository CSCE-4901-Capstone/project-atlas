import React, {useState,useEffect} from "react";        // import the useState and useEffect to generate Session Tokens
import ChoiceCountry from './ChoiceCountry'
import api_conn from 'src/utils/api';
/*
AI logic functionality will be inserted here then put the variable for the return prompt in the brackets where the comment is and 
delete filler text
 */

const AISummary = ({choiceCountry}) =>{
    const[AI_Response, SET_AI_Response] = useState("Getting AI Response...");   //declaring what to display while response is getting fetched
    const[SessionNum, SET_SessionNum] = useState("");

    //for testing purposes manually set value of choiceCountry below (uncomment when not needed)
    choiceCountry = "USA";
    
    //Use effect to make a call to the server
        useEffect(() => {
            const NEW_SessionNum = crypto.randomUUID(); //use built in crypto tool to randomly generate a Session ID (for database purposes)
            SET_SessionNum(NEW_SessionNum); //Store the newly generated Session ID to the current use State
            async function GET_AI_Response() {
                await api_conn.post("/api/AI/", {       //sending post request with needed values in body
                    country: choiceCountry,
                    session_id: SessionNum,
                    Role_choice: 0
                })
                    /*?country=${choiceCountry}/${SessionNum}`).then(response => response.data) .then(data => {
                    console.log(data);
                    SET_AI_Response(data.response);
                  })*/
                .then(response => {
                    console.log("AI response received:", response.data);
                    SET_AI_Response(response.data.response);
                })
                .catch(error => console.error('Error fetching json file:', error));
            }
            try{
                if(choiceCountry){
                    GET_AI_Response();
                    console.log(AI_Response);
                }
            } catch (e) {
                console.error(e);
            }


        }, []);

    return(
        <>
            <ChoiceCountry choice={choiceCountry}/>
            <div className="text-container">
                <p>
                    {SessionNum != "" ? AI_Response : "Getting AI Response..."}
                </p>
            </div>
        </>
    )
}

export default AISummary;
