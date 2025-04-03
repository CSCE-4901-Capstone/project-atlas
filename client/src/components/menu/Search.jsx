import { useState, useEffect } from "react";

//Array is dummy data that tests the suggestion functionality
const COUNTRIES = ["Afghanistan", "Angola", "Albania", "United Arab Emirates", "Argentina", "Armenia", "Fr. S. Antarctic Lands", "Australia", "Austria", "Azerbaijan", "Burundi", "Belgium", "Benin", "Burkina Faso", "Bangladesh", "Bulgaria", "Bahamas", "Bosnia and Herz.", "Belarus", "Belize", "Bolivia", "Brazil", "Brunei", "Bhutan", "Botswana", "Central African Rep.", "Canada", "Switzerland", "Chile", "China", "Côte d'Ivoire", "Cameroon", "Dem. Rep. Congo", "Congo", "Colombia", "Costa Rica", "Cuba", "N. Cyprus", "Cyprus", "Czech Rep.", "Germany", "Djibouti", "Denmark", "Dominican Rep.", "Algeria", "Ecuador", "Egypt", "Eritrea", "Spain", "Estonia", "Ethiopia", "Finland", "Fiji", "Falkland Is.", "France", "Gabon", "United Kingdom", "Georgia", "Ghana", "Guinea", "Gambia", "Guinea-Bissau", "Eq. Guinea", "Greece", "Greenland", "Guatemala", "Guyana", "Honduras", "Croatia", "Haiti", "Hungary", "Indonesia", "India", "Ireland", "Iran", "Iraq", "Iceland", "Israel", "Italy", "Jamaica", "Jordan", "Japan", "Kazakhstan", "Kenya", "Kyrgyzstan", "Cambodia", "Korea", "Kosovo", "Kuwait", "Lao PDR", "Lebanon", "Liberia", "Libya", "Sri Lanka", "Lesotho", "Lithuania", "Luxembourg", "Latvia", "Morocco", "Moldova", "Madagascar", "Mexico", "Macedonia", "Mali", "Myanmar", "Montenegro", "Mongolia", "Mozambique", "Mauritania", "Malawi", "Malaysia", "Namibia", "New Caledonia", "Niger", "Nigeria", "Nicaragua", "Netherlands", "Norway", "Nepal", "New Zealand", "Oman", "Pakistan", "Panama", "Peru", "Philippines", "Papua New Guinea", "Poland", "Puerto Rico", "Dem. Rep. Korea", "Portugal", "Paraguay", "Palestine", "Qatar", "Romania", "Russia", "Rwanda", "W. Sahara", "Saudi Arabia", "Sudan", "S. Sudan", "Senegal", "Solomon Is.", "Sierra Leone", "El Salvador", "Somaliland", "Somalia", "Serbia", "Suriname", "Slovakia", "Slovenia", "Sweden", "Swaziland", "Syria", "Chad", "Togo", "Thailand", "Tajikistan", "Turkmenistan", "Timor-Leste", "Trinidad and Tobago", "Tunisia", "Turkey", "Taiwan", "Tanzania", "Uganda", "Ukraine", "Uruguay", "United States", "Uzbekistan", "Venezuela", "Vietnam", "Vanuatu", "Yemen", "South"]

  

const Search = ({onChangeHandle}) => {
    //Filter Array for displaying suggestions based on the entered input    
    const [filteredSuggestions, setFilteredSuggestions] = useState([]);
    const [input, setInput] = useState('');
    const [showOptions, setShowOptions] = useState(false);
    const [error,setError] = useState(false);

    const handleSearchInput = (event) => {
        //Allows user to press enter on key to submit search value
        if(event.key === 'Enter' && error != true){
            if(filteredSuggestions.includes(event.target.value)){
                onChangeHandle(event.target.value);
                setFilteredSuggestions([]);
                setShowOptions(false);
                setError(false);
            }
        }
      };

    const handleChange = (e) => {
        //Suggest countries from a list of available coutries
        const value = e.target.value;
        setInput(value);

        if(value){
            setFilteredSuggestions(COUNTRIES.filter((item)=> item.toLowerCase().startsWith(value.toLowerCase())));
            setShowOptions(true);
            setError(filteredSuggestions.length == 0);
        } else {
            setFilteredSuggestions([]);
            setShowOptions(false);
            setError(false);
        }
    }
    const handleItemClick = (value) => {
        //If suggestion is clicked, list disappears and the menu value of the choice country is updated while input value is updated
        onChangeHandle(value);
        setInput(value);
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
