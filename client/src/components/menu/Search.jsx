import { useState, useEffect } from "react";

//Array is dummy data that tests the suggestion functionality
const Countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria",
    "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
    "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia",
    "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica",
    "Croatia", "Cuba", "Cyprus", "Czechia (Czech Republic)", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador",
    "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini (Swaziland)", "Ethiopia", "Fiji", "Finland", "France",
    "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau",
    "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland",
    "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait",
    "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg",
    "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico",
    "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar (Burma)", "Namibia", "Nauru",
    "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman",
    "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal",
    "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
    "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia",
    "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria",
    "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan",
    "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City",
    "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
  ];
  

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
            } else {
                
            }
        }
      };

    const handleChange = (e) => {
        //Suggest countries from a list of available coutries
        const value = e.target.value;
        setInput(value);

        if(value){
            setFilteredSuggestions(Countries.filter((item)=> item.toLowerCase().startsWith(value.toLowerCase())));
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