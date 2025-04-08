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

      // Fake temperature values (-30°C to 50°C) from west to east
      const tempMin = -30;
      const tempMax = 50;
      const scale = chroma.scale(['#0000ff', '#00ffff', '#ffff00', '#ff0000']).domain([tempMin, tempMax]);

      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          const i = (y * width + x) * 4;

          // Test temp (to be pulled from json file)
          const temp = tempMin + (x / width) * (tempMax - tempMin) * (1 - Math.abs((y - height / 2) / (height / 2)));

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

