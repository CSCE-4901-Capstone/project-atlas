import React, {useState,useEffect, useRef} from "react";        // import the useState and useEffect to generate Session Tokens
import ChoiceCountry from './ChoiceCountry'
import api_conn from 'src/utils/api';
/*
AI logic functionality will be inserted here then put the variable for the return prompt in the brackets where the comment is and 
delete filler text
 */

const AISummary = ({chCountry}) =>{
    const[AI_Response, SET_AI_Response] = useState("Select a country for a list of news Articles");   //declaring what to display while response is getting fetched
    const[SessionNum, SET_SessionNum] = useState("");
    const[articleArray, setArticleArray] = useState([]);
    //useref for single calls only Note: useEffect in React 18 causes double fetch calls for debugging purposes and will not be affected in production
    //Use effect to make a call to the server
        useEffect(() => {
            const NEW_SessionNum = crypto.randomUUID(); //use built in crypto tool to randomly generate a Session ID (for database purposes)
            SET_SessionNum(NEW_SessionNum); //Store the newly generated Session ID to the current use State

            

            //async function to grab data
            async function GET_AI_Response() {
                await api_conn.post("/api/AI/", {       //sending post request with needed values in body
                    country: chCountry,
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
                        if(response.data.response != "AI response not received"){
                            const parsed = JSON.parse(response.data.response).articles;
                            console.log(parsed);
                            setArticleArray(parsed);
                        }
                })
                .catch(error => console.error('Error fetching json file:', error));
            }
            try{
                console.log(chCountry)
                if(chCountry){
                    GET_AI_Response();
                }
            } catch (e) {
                console.error(e);
            }
        }, [chCountry]);
        //useEffect to test if the parsed article array works
        useEffect(() => {
            console.log(articleArray);
        }, [articleArray])

    return(
        <>
            <ChoiceCountry choice={chCountry}/>
            <div className="text-container">
                <ul className="article">
                    {articleArray.length > 0 ? articleArray.map((item) => (
                        <li key={item.title}>
                            <h3><a href={item.link} target="_blank" rel="noopener noreferrer">{item.title}</a></h3>
                            <p>{item.description}</p>
                            <p>Source: <strong>{item.source}</strong></p>
                        </li>
                    )): "Please Select a country..."}
                </ul>
            </div>
        </>
    )
}

export default AISummary;
