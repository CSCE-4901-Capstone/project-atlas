import { useEffect, useState } from 'react';
import { useLoader } from '@react-three/fiber';
import { TextureLoader, CanvasTexture, LinearFilter, LinearMipMapLinearFilter } from 'three';
import { OrbitControls } from '@react-three/drei';
import chroma from 'chroma-js';

function Weather() {
  const [tempTexture, setTempTexture] = useState(null);
  const fallbackTexture = useLoader(TextureLoader, '/images/earth2.jpg');

  useEffect(() => {
    const generateTemperatureTexture = async () => {
      const width = 360;
      const height = 180;
      const canvas = document.createElement('canvas');
      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext('2d');
      const imageData = ctx.createImageData(width, height);

      // Fake temperature values
      const tempMin = -98;
      const tempMax = 60;
      const scale = chroma.scale([
        '#4200ff',  // Very cold (deep purple)
        '#0061ff',  // Cold (blue)
        '#00d5ff',  // Cool (light blue)
        '#a0ddff',  // Slightly cool
        '#ffffff',  // Neutral (white) - centered around 21-23°C
        '#ffffcc',  // Slightly warm
        '#ffff00',  // Warm (yellow)
        '#ff8000',  // Hot (orange)
        '#ff0000'   // Very hot (red)
      ]).domain([
        tempMin,    // -98°C
        0,          // 0°C (freezing)
        15,         // Cool
        21,         // Start of ideal range
        23,         // Middle of ideal range
        25,         // End of ideal range
        30,         // Warm
        40,         // Hot
        tempMax     // 60°C
      ]);

      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          const i = (y * width + x) * 4;

          // Test temp (to be pulled from json file)
          const temp = -82;

          const [r, g, b] = scale(temp).rgb();
          imageData.data[i] = r;
          imageData.data[i + 1] = g;
          imageData.data[i + 2] = b;
          imageData.data[i + 3] = 255;
        }
      }

      ctx.putImageData(imageData, 0, 0);
      const tex = new CanvasTexture(canvas);
      tex.minFilter = LinearMipMapLinearFilter;
      //tex.generateMipmaps = false;
      tex.needsUpdate = true;
      setTempTexture(tex);
    };

    generateTemperatureTexture();
  }, []);

  return (
    <>
      <ambientLight intensity={1} />
      <OrbitControls makeDefault />
      <mesh>
        <sphereGeometry args={[2, 450, 450]} />
        <meshStandardMaterial map={tempTexture || fallbackTexture}
        transparent={true}
        opacity={0.7} 
        />
      </mesh>
    </>
  );
}

export default Weather;

