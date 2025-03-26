import { useState, useEffect } from "react";


const Search = ({onChangeHandle}) => {
    const handleSearchChange = (event) => {
        onChangeHandle(event.target.value);
      };
    return(
        <>
           <div id="search">
                <input
                    type="text"
                    placeholder="Search for a Country"
                    onChange={handleSearchChange}
                />
            </div>
        </>

    )
}

export default Search;