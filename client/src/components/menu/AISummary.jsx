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

    const NEW_SessionNum = crypto.randomUUID(); //use built in crypto tool to randomly generate a Session ID (for database purposes)
    SET_SessionNum(NEW_SessionNum); //Store the newly generated Session ID to the current use State
    
    //Use effect to make a call to the server
        useEffect(() => {
            async function Get_AI_Response() {
                await api_conn.get(`/api/AI?country=${choiceCountry}/${SessionNum}`).then(response => response.data) .then(data => {
                    console.log(data);
                    SET_AI_Response(data.response);
                  })
                  .catch(error => console.error('Error fetching json file:', error));
                }
          Get_AI_Response();
        }, []);

    return(
        <>
            <ChoiceCountry choice={choiceCountry}/>
            <div className="text-container">
                <p>
                    {AI_Response}
                </p>
            </div>
        </>
    )
}

export default AISummary;
