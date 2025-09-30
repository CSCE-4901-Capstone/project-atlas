import { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import StarField from 'src/components/StarField';
import CountryHighlight from 'src/components/builders/CountryHighlight';
import CameraController from 'src/components/CameraController';
import Flights from 'src/components/builders/Flights';
import UpdateFilter from 'src/components/builders/UpdateFilter'
import Globe from 'src/components/Globe';

function Environment({ selectedCountry, onCountrySelection, activeFilter }) {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });
  const [clickDisabled, setClickDisabled] = useState(false);

  useEffect(() => {
    function handleResize() {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight
      });
    }

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <Canvas
      style={{
        width: windowSize.width,
        height: windowSize.height,
        background: 'black',
        pointerEvents: clickDisabled ? 'none' : 'auto'
      }}
    >
      <StarField numStars={500}/>
      <CameraController
        selectedCountry={selectedCountry}
        setClickDisabled={setClickDisabled}
      />
      <OrbitControls 
        makeDefault 
        enablePan={false}
        minDistance={3} 
        maxDistance={5}
      />
      <UpdateFilter activeFilter={activeFilter} />
      <CountryHighlight selectedCountry={selectedCountry}/>
      <Globe onCountrySelection={onCountrySelection}/>
    </Canvas>
  )
}

export default Environment;
