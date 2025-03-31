import { useState } from 'react';
import Environment from 'src/components/Environment';
import 'src/styles/Atlas.css';
import Menu from '../components/menu/Menu';

function Atlas() {
  let [selectedCountry, setSelectedCountry] = useState(null)

  return (
    <>
      <Environment selectedCountry={selectedCountry} onCountrySelection={setSelectedCountry}/>
      <Menu/>
    </>
  )
}

export default Atlas
