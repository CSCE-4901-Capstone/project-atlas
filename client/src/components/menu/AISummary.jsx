import React from "react";
import ChoiceCountry from './ChoiceCountry'

/*
AI logic functionality will be inserted here then put the variable for the return prompt in the brackets where the comment is and 
delete filler text
 */

const AISummary = ({choiceCountry}) =>{
    return(
        <>
            <ChoiceCountry choice={choiceCountry}/>
            <p>
                {/*Insert AI prompt return here and delete below filler text */}
                International Relations and Politics Ukraine-Russia Ceasefire Negotiations: Ukrainian President Volodymyr Zelenskyy has called on U.S. President Donald Trump to 
                leverage America's influence to press Russia into accepting a ceasefire in Ukraine. While U.S.-Russia talks have made some progress, significant challenges and 
                mistrust persist. Russian President Vladimir Putin has suggested that Ukrainian troops in the Kursk region could surrender safely, but Zelenskyy remains skeptical 
                of Russia’s intentions, accusing Putin of obstructing the peace process.
                Global Leaders Advocate for Peace in Ukraine: Australian
            </p>
        </>
    )
}

export default AISummary;
