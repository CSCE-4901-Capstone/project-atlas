import { useState } from 'react';
import { useLoader } from '@react-three/fiber';
import * as THREE from 'three';
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

    if (timeDiff < 100) {
      let selectedCountry = await getSelectedCountry(e.point)
      onCountrySelection(selectedCountry)
      console.log(selectedCountry)
    }

    setPointerDownTime(null);
  }

  // Loads the earth texture
  const [map, specularMap, bumpMap] = useLoader(THREE.TextureLoader, [
    "/images/earth2.jpg",
    "/images/02_earthspec1k.jpg",
    "/images/01_earthbump1k.jpg",
  ]);

  map.colorSpace = THREE.SRGBColorSpace
  //texture.minFilter = LinearFilter;
  //texture.generateMipmaps = false;
  //texture.needsUpdate = true;

  return (
    <>
      <ambientLight intensity={3} />
      <mesh 
        onPointerDown={handlePointerDown}
        onPointerUp={handlePointerUp}
      >
          <sphereGeometry args={[2, 51, 32]} />
          <meshPhongMaterial
            map={map}
            specularMap={specularMap}
            bumpMap={bumpMap}
            bumpScale={0.04}
          />
      </mesh>
    </>
  )
}

export default Globe;
