import React, {useState,useEffect, useRef} from "react";        // import the useState and useEffect to generate Session Tokens
import ChoiceCountry from './ChoiceCountry'
import api_conn from 'src/utils/api';
/*
AI logic functionality will be inserted here then put the variable for the return prompt in the brackets where the comment is and 
delete filler text
 */

const News = ({chCountry}) =>{
    //const[AI_Response, SET_AI_Response] = useState("Select a country for a list of news Articles");   //declaring what to display while response is getting fetched
    
    const[articleArray, setArticleArray] = useState([]);
    const[statusText, setStatusText] = useState("Please select a country... ");

    //useref for single calls only Note: useEffect in React 18 causes double fetch calls for debugging purposes and will not be affected in production
    //Use effect to make a call to the server
        useEffect(() => {
            if (!chCountry){
                setArticleArray([]);setStatusText("Please select a country... ");
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
                                setStatusText("Array populated!")
                            }

                            /*if(response.data.response != "AI response not received"){
                                const parsed = JSON.parse(response.data.response).articles;
                                console.log(parsed);
                                setArticleArray(parsed);
                            }*/
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
    <div className="text-container">
      {articleArray.length > 0 ? (
        <ul className="article">
          {articleArray.map((item, idx) => (
            <li key={item?.link ?? `${idx}`}>
                
              <h3>
                {(item?.Num ?? idx + 1)}{" "}
                <a
                  href={item?.link ?? "#"}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {item?.Title ?? "Untitled"}
                </a>
              </h3>

              {item?.Author ? <p>By {item.Author}</p> : null}
              {item?.Timestamp ? <p>{item.Timestamp}</p> : null}
            </li>
          ))}
        </ul>
      ) : (
        <p>{statusText}</p>
      )}
    </div>
  </>
);
};

export default News;

