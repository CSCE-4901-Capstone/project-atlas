import { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import StarField from 'src/components/StarField';
import CountryHighlight from 'src/components/builders/CountryHighlight'
import Flights from 'src/components/builders/Flights'
import Globe from 'src/components/Globe';

function Environment({selectedCountry, onCountrySelection}) {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });

  function handleResize() {
    setWindowSize({
      width: window.innerWidth,
      height: window.innerHeight
    });
  }

  // Handles screen resizing
  useEffect(() => {
    window.addEventListener('resize', handleResize)
  }, [])

  return (
    <Canvas
      style={{ width: windowSize.width, height: windowSize.height, background: 'black'}}
    >
      <StarField numStars={500}/>
      <CountryHighlight selectedCountry={selectedCountry}/>
      <Globe onCountrySelection={onCountrySelection}/>
    </Canvas>
  )
}

export default Environment;
