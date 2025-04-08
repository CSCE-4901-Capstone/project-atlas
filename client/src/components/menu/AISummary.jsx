import React, {useState,useEffect} from "react";        // import the useState and useEffect to generate Session Tokens
import ChoiceCountry from './ChoiceCountry'

/*
AI logic functionality will be inserted here then put the variable for the return prompt in the brackets where the comment is and 
delete filler text
 */

const AISummary = ({choiceCountry}) =>{
    const[AI_Response, SET_AI_Response] = useState("Getting AI Response...");   //declaring what to display while response is getting fetched
    const[SessionNum, SET_SessionNum] = useState("")

    const NEW_SessionNum = crypto.randomUUID(); //use built in crypto tool to randomly generate a Session ID (for database purposes)
    SET_SessionNum(NEW_SessionNum); //Store the newly generated Session ID to the current use State

    useEffect(() => {
        const Get_AI_Response = async () => {
            try{
                //This is where the AI logic will be inserted
                //For this example, let's assume we're making a GET request to an AI endpoint
                const response = await fetch(`http://127.0.0.1:8000/api/AI/`);
                const AI_Response_Data = await response.json();
                SET_AI_Response(AI_Response_Data.response);

            } catch (e){
                console.error(e)
            }

        }

        if(choiceCountry) {
            Get_AI_Response();  //Call the function when the choiceCountry state changes (ensuring new data is generated from API)
        }
    })

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
