import { useState } from 'react';
import Environment from 'src/components/Environment';
import 'src/styles/Atlas.css';
import Menu from '../components/menu/Menu';
import Welcome from '../components/menu/Welcome'

function Atlas() {
  const [activeFilter, setActiveFilter] = useState(null);
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [showWelcome,setShowWelcome] = useState(true);

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
      {showWelcome && <Welcome onClose={() => setShowWelcome(false)}/>}
    </>
  )
}

export default Atlas;
