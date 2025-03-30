import { useEffect, useState } from 'react';
import { Canvas, useLoader} from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { TextureLoader, LinearFilter, FogExp2 } from 'three';
import StarField from 'src/components/StarField';
import getSelectedCountry from 'src/utils/GetSelectedCountry'
import Outline from 'src/components/builders/Outline'
import Flights from 'src/components/builders/Flights'
//import Movement from 'src/components/Movement'

function Globe() {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });
  const [pointerDownTime, setPointerDownTime] = useState(null);

  function handleResize() {
    setWindowSize({
      width: window.innerWidth,
      height: window.innerHeight
    });
  }

  // When the mouse is down, its reset the dragging and get the time
  function handlePointerDown() {
    setPointerDownTime(Date.now());
  }
  
  // When it goes up, check how long its been down and whether it's been dragging
  async function handlePointerUp(e) {
    const timeDiff = Date.now() - pointerDownTime;

    if (timeDiff < 200) {
      let selectedCountry = await getSelectedCountry(e.point)
      console.log(selectedCountry)
    }

    setPointerDownTime(null);
  }

  useEffect(() => {
    window.addEventListener('resize', handleResize)
  }, [])

  const texture= useLoader(TextureLoader, "/images/earth2.jpg");
  texture.minFilter = LinearFilter;
  texture.generateMipmaps = false;
  texture.needsUpdate = true;

  return (
    <Canvas
      style={{ width: windowSize.width, height: windowSize.height, background: 'black'}}
    >
      <ambientLight intensity={3} />
      <StarField numStars={500}/>
      <Outline filename={'countries.json'} radius={2}/>
      <OrbitControls makeDefault/>
      <mesh 
        onPointerDown={handlePointerDown}
        onPointerUp={handlePointerUp}
      >
          <sphereGeometry args={[2, 51, 32]} />
          <meshStandardMaterial map={texture} />
      </mesh>
    </Canvas>
  )
}

export default Globe;
