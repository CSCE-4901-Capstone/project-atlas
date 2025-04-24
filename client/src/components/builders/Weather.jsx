import { useEffect, useState } from 'react';
import { useLoader } from '@react-three/fiber';
import { TextureLoader, CanvasTexture, LinearMipMapLinearFilter, RepeatWrapping, ClampToEdgeWrapping } from 'three';
import chroma from 'chroma-js';

function Weather() {
  const [tempTexture, setTempTexture] = useState(null);
  const fallbackTexture = useLoader(TextureLoader, '/images/earth2.jpg');

  useEffect(() => {
    const generateTemperatureTexture = async () => {
      const res = await fetch('http://localhost:8000/api/weather/');
      const json = await res.json();
      const grid = json.data;

      const height = grid.length;
      const width = grid[0]?.length || 0;

      const canvas = document.createElement('canvas');
      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext('2d');
      const imageData = ctx.createImageData(width, height);

      const tempMin = -50;
      const tempMax = 40;

      const scale = chroma.scale([
        '#000080', // Navy Blue (~ -50°C)
        '#0055cc', // Sky Blue (~ -20°C)
        '#00ccff', // Cyan (~ 0°C)
        '#66ffcc', // Light Green (~ 10°C)
        '#ffff99', // Pale Yellow (~ 20°C)
        '#ffcc66', // Light Orange (~ 25°C)
        '#ff6600', // Orange (~ 30°C)
        '#cc0000'  // Deep Red (~ 40°C)
      ]).domain([tempMin, -20, 0, 10, 20, 25, 30, tempMax]);


      // Flip Y axis: top of canvas should be lat +90 (North Pole)
      for (let y = 0; y < height; y++) {
        const flippedY = height - 1 - y;
        for (let x = 0; x < width; x++) {
          const i = (y * width + x) * 4;
          const temp = grid[flippedY][x]; // flip Y here

          const [r, g, b] = scale(temp ?? tempMin).rgb();
          imageData.data[i] = r;
          imageData.data[i + 1] = g;
          imageData.data[i + 2] = b;
          imageData.data[i + 3] = 255;
        }
      }

      ctx.putImageData(imageData, 0, 0);
      const tex = new CanvasTexture(canvas);
      tex.minFilter = LinearMipMapLinearFilter;
      //tex.wrapS = RepeatWrapping; // horizontal wrapping
      //tex.wrapT = ClampToEdgeWrapping; // no vertical wrapping
      tex.needsUpdate = true;
      setTempTexture(tex);
    };

    generateTemperatureTexture();
  }, []);

  return (
    <mesh>
      <sphereGeometry args={[2, 51, 32]} />
      <meshStandardMaterial map={tempTexture || fallbackTexture} />
    </mesh>
  );
}

export default Weather;
