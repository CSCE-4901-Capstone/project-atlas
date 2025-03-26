import { useState, useEffect } from "react";


const Search = ({onChangeHandle}) => {
    const handleSearchInput = (event) => {
        if(event.key === 'Enter'){
            onChangeHandle(event.target.value);
        }
      };
    return(
        <>
           <div id="search">
                <input
                    type="text"
                    placeholder="Search for a Country"
                    onKeyDown={handleSearchInput}
                />
            </div>
        </>

    )
}

export default Search;