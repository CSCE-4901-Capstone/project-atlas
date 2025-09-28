import React, {useState,useEffect, useRef} from "react";        // import the useState and useEffect to generate Session Tokens
import ChoiceCountry from './ChoiceCountry'
import api_conn from 'src/utils/api';
import loadingGif from "../../assets/loading.gif"
/*
AI logic functionality will be inserted here then put the variable for the return prompt in the brackets where the comment is and 
delete filler text
 */




const News = ({chCountry}) =>{
    const[articleArray, setArticleArray] = useState([]);
    const[statusText, setStatusText] = useState("Please select a country... ");

    //useref for single calls only Note: useEffect in React 18 causes double fetch calls for debugging purposes and will not be affected in production
    //Use effect to make a call to the server
        useEffect(() => {
            if (!chCountry){
                setArticleArray([]);
                setStatusText("Please select a country... ");
                return;
            }
        
            const SessionID = crypto.randomUUID(); //use built in crypto tool to randomly generate a Session ID (for database purposes)


            //async function to grab data
            function GET_NEWS_response() {
                setStatusText("fetching articles from NEWS_API")
                
                api_conn.post("/api/AI/", {       //sending post request with needed values in body
                    country: chCountry,
                    session_id: SessionID,
                    Role_choice: 0                  //can actually remove later on
                    })
                    .then(response => {
                            console.log("response FROM views.py:", response.data);
                            const articles = response?.data?.articles ?? [];
                            //SET_AI_Response(response.data.response);
                            if (Array.isArray(articles) && articles.length > 0){
                                setArticleArray(articles);
                                //Prevents loading gif from being at the bottom of the articles
                                setStatusText("");
                            }
                            else{
                            setArticleArray([]);
                            setStatusText("No articles found/no response form API...")
                            }
                    })
                    .catch((error) => {
                        console.error('Error fetching json file:', error);
                        setArticleArray([]);
                        setStatusText("There was an error when fetching the articles");

                    });
                }
    
                GET_NEWS_response();
        }, [chCountry]);

return (
  <>
    <ChoiceCountry choice={chCountry} />
    <div id="text-container" >
    {articleArray.length > 0 ? (
        <ol className="article">
        {articleArray.map((item, idx) => {
            const safeTitle =
            (item?.title && item.title.trim()) ||
            (item?.source && `(${item.source})`) ||
            "Untitled";
            return (
            <li key={item?.link ?? `${idx}`} style ={{marginBottom: "1rem"}}>
                <h3>
                    {idx+1}. {" "}
                <a
                    href={item?.link ?? "#"}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{ color: "#00FFFF", textDecoration: "none" }}  // link color here
                >
                    {safeTitle}
                </a>
                </h3>
                {item?.description ? <p>{item.description}</p> : null}
                {item?.source ? (
                <p>
                    Source: <strong>{item.source}</strong>
                </p>
                ) : null}
            </li>
            );
        })}
        </ol>
    ) : null}
    {statusText == "fetching articles from NEWS_API" ? (
        <img id="loading-gif" src={loadingGif} alt="loading gif"/>
    ) : (
        <p>{statusText}</p>
    )}
    </div>
  </>
  
);
};

export default News;

