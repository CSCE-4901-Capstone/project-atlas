import { useState } from 'react';
import Environment from 'src/components/Environment';
import 'src/styles/Atlas.css';
import Menu from '../components/menu/Menu';

function Atlas() {
  const [activeFilter, setActiveFilter] = useState(null);
  const [selectedCountry, setSelectedCountry] = useState(null);

  return (
    <>
      <Environment 
        selectedCountry={selectedCountry} 
        onCountrySelection={setSelectedCountry} 
        activeFilter={activeFilter}
      />
      <Menu 
        searchVal={selectedCountry} 
        setSearchVal={setSelectedCountry} 
        onFilterSelection={setActiveFilter} //Update toggle 
        activeFilter={activeFilter} 
      />
    </>
  )
}

export default Atlas;
