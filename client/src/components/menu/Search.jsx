import { useState, useEffect } from "react";
import { label } from "three/tsl";

//Array is dummy data that tests the suggestion functionality
const Countries = ['United States', 'Japan', 'South Korea', 'Mexico', 'Canada', 'Australia', 'United Kingdom'];

const Search = ({onChangeHandle}) => {
    //Filter Array for displaying suggestions based on the entered input    
    const [filteredSuggestions, setFilteredSuggestions] = useState([]);
    const [input, setInput] = useState('');
    const [showOptions, setShowOptions] = useState(false);
    const [error,setError] = useState(false);

    const handleSearchInput = (event) => {
        //Allows user to press enter on key to submit search value
        if(event.key === 'Enter' && error != true){
            onChangeHandle(event.target.value);
            setFilteredSuggestions([]);
            setShowOptions(false);
            setError(false);
        }
      };
    const handleChange = (e) =>{
        //Suggest countries from a list of available coutries
        const value = e.target.value;
        setInput(value);

        if(value){
            setFilteredSuggestions(Countries.filter((item)=> item.toLowerCase().startsWith(value.toLowerCase())));
            setShowOptions(filteredSuggestions.length > 0);
            setError(filteredSuggestions.length === 0);
        } else {
            setFilteredSuggestions([]);
            setShowOptions(false);
            setError(false);
        }
    }
    const handleItemClick = (value) => {
        //If suggestion is clicked, list disappears and the menu value of the choice country is updated while input value is updated
        onChangeHandle(value)
        setInput(value)
        setShowOptions(false);
        setError(false);
    }
    return(
        <>
           <div id="search">
                <input
                    id="search-input"
                    type="text"
                    placeholder="Search for a Country"
                    value={input}
                    onKeyDown={handleSearchInput}
                    onChange={handleChange}
                />
                {showOptions && filteredSuggestions.length > 0 && (
                    <ul className="suggestion-list">
                        {filteredSuggestions.map((option, index) => (
                            <li
                                key={index}
                                className="suggestion-item"
                                onClick={() => handleItemClick(option)}
                            >
                                {option}
                            </li>
                        ))}
                    </ul>
                )}
                {input.length > 1 && error && <p className="error-message">Please select a valid Country</p>}
            </div>
        </>

    )
}

export default Search;