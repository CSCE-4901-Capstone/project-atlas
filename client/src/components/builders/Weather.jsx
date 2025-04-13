import { useLoader } from '@react-three/fiber';
import { TextureLoader } from 'three';
import { OrbitControls } from '@react-three/drei';

function Weather() {
  // Load the stitched global weather texture
  const weatherTexture = useLoader(TextureLoader, '/stitched_weather.png');
  
  // Optional fallback if the main texture fails (e.g., local earth map)
  const fallbackTexture = useLoader(TextureLoader, '/images/earth2.jpg');

  return (
    <>
      <ambientLight intensity={1} />
      <OrbitControls makeDefault />
      <mesh>
        <sphereGeometry args={[2, 128, 128]} />
        <meshStandardMaterial
          map={weatherTexture || fallbackTexture}
        />
      </mesh>
    </>
  );
}

export default Weather;

