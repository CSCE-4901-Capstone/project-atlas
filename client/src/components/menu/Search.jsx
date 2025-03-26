import { useState, useEffect } from "react";
import ChoiceCountry from "./ChoiceCountry";

function Search() {
    const [choice,setChoice] = useState('');
    //Helper functions
    const formSubmit = () =>{
        console.log(choice)
    }
    //Function to work around form submit for our input as we only need the one piece of information
    const handleEnter = (e) =>{
        if(e.key === 'Enter'){
            e.preventDefault();
            formSubmit();
        }
    }

    return(
        <>
           <div id="search">
                <input
                    type="text"
                    value={choice}
                    placeholder="Search for a Country"
                    onChange={(e)=>{setChoice(e.target.value)}}
                    onKeyDown={handleEnter}
                />
            </div>
        </>

    )
}

export default Search;