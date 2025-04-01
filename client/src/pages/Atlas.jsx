import { useState } from 'react';
import Environment from 'src/components/Environment';
import 'src/styles/Atlas.css';
import Menu from '../components/menu/Menu';

function Atlas() {
  let [selectedCountry, setSelectedCountry] = useState(null);
  let [activeFilter, setActiveFilter] = useState(null);

  return (
    <>
      <Environment selectedCountry={selectedCountry} onCountrySelection={setSelectedCountry} activeFilter={activeFilter}/>
      <Menu searchVal={selectedCountry} setSearchVal={setSelectedCountry} onFilterSelection={setActiveFilter}/>
    </>
  )
}

export default Atlas
