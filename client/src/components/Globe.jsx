import { useState } from 'react';
import { useLoader } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { TextureLoader, LinearFilter } from 'three';
import getSelectedCountry from 'src/utils/GetSelectedCountry';
//import Movement from 'src/components/Movement'

function Globe({onCountrySelection = () => {}}) {
  const [pointerDownTime, setPointerDownTime] = useState(null);

  // When the mouse is down, its reset the dragging and get the time
  function handlePointerDown() {
    setPointerDownTime(Date.now());
  }
  
  // When it goes up, check how long its been down and whether it's been dragging
  async function handlePointerUp(e) {
    const timeDiff = Date.now() - pointerDownTime;

    if (timeDiff < 200) {
      let selectedCountry = await getSelectedCountry(e.point)
      onCountrySelection(selectedCountry)
      console.log(selectedCountry)
    }

    setPointerDownTime(null);
  }

  // Loads the earth texture
  const texture = useLoader(TextureLoader, "/images/earth2.jpg");
  texture.minFilter = LinearFilter;
  texture.generateMipmaps = false;
  texture.needsUpdate = true;

  return (
    <>
      <ambientLight intensity={3} />
      <OrbitControls makeDefault/>
      <mesh 
        onPointerDown={handlePointerDown}
        onPointerUp={handlePointerUp}
      >
          <sphereGeometry args={[2, 51, 32]} />
          <meshStandardMaterial map={texture} />
      </mesh>
    </>
  )
}

export default Globe;
