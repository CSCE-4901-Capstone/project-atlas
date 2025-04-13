import { useLoader } from '@react-three/fiber';
import { TextureLoader } from 'three';
import { OrbitControls } from '@react-three/drei';

function Weather() {
  // palette '-98:4200ff;0:0061ff;15:00d5ff;21:a0ddff;23:ffffff;25:ffffcc;30:ffff00;40:ff8000;60:ff0000';
  const apiKey = ''; // API key goes her and we're going to use .env in production!
  const weatherUrl = `https://tile.openweathermap.org/map/temp_new/1/1/1.png?appid=${apiKey}&palette=-98:4200ff;0:0061ff;15:00d5ff;21:a0ddff;23:ffffff;25:ffffcc;30:ffff00;40:ff8000;60:ff0000`;

  const weatherTexture = useLoader(TextureLoader, weatherUrl);
  const fallbackTexture = useLoader(TextureLoader, '/images/earth2.jpg');

  return (
    <>
      <ambientLight intensity={1} />
      <OrbitControls makeDefault />
      <mesh>
        <sphereGeometry args={[2, 450, 450]} />
        <meshStandardMaterial
          map={weatherTexture || fallbackTexture}
        />
      </mesh>
    </>
  );
  }

export default Weather;