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
      //const width = 360;
      //const height = 180;
      const res = await fetch('http://localhost:8000/api/weather/');
      const json = await res.json();
      const grid = json.data;
      const width = json.lon;
      const height = json.lat;

      const canvas = document.createElement('canvas');
      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext('2d');
      const imageData = ctx.createImageData(width, height);

      // Fake temperature values
      const tempMin = -50;
      const tempMax = 40;

      const scale = chroma.scale([
        '#4200ff',  // Very cold (deep purple)
        '#0061ff',  // Cold (blue)
        '#00d5ff',  // Cool (light blue)
        '#90eb9d',  // Slightly cool (light Green)
        '#ffffbf',  // Neutral 
        '#f9d057',  // Slightly warm
        '#f29e2e',  // Warm (yellow)
        '#e76818',  // Hot (orange)
        '#d7191c'   // Very hot (red)
      ]).domain([
        tempMin,    // -50°C
        -20,         // cold (-20)
        0,         // freezing (0)
        15,         // Mild
        20,         // Ideal/Neutral
        23,         // Slightly Warm
        25,         // Warm
        30,         // Hot
        tempMax     //  (40+)°C
      ]);

      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          const i = (y * width + x) * 4;
          const temp = grid[y][x];

          // Test temp (to be pulled from json file)
         // const temp = -82;

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
      //tex.generateMipmaps = false;
      tex.needsUpdate = true;
      setTempTexture(tex);
    };

    generateTemperatureTexture();
  }, []);

  return (
    <>
      <mesh>
        <sphereGeometry args={[2, 450, 450]} />
        <meshStandardMaterial map={tempTexture || fallbackTexture}
        />
      </mesh>
    </>
  );
}

export default Weather;