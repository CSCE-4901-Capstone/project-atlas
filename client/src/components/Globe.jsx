import { useEffect, useState } from 'react';
import { Canvas, useLoader} from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { TextureLoader, LinearFilter, FogExp2 } from 'three';
import StarField from 'src/components/StarField';
import Outline from 'src/components/builders/Outline'
//import Movement from 'src/components/Movement'

function Globe() {
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
      <Outline filename={'countries.json'} radius={2.05}/>
      <OrbitControls />
      <mesh>
          <sphereGeometry args={[2, 51, 32]} />
          <meshStandardMaterial map={texture} />
      </mesh>
    </Canvas>
  )
}

export default Globe;
