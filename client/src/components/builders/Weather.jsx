import { useEffect, useState } from 'react';
import { useLoader } from '@react-three/fiber';
import { TextureLoader, CanvasTexture, LinearMipMapLinearFilter } from 'three';
import chroma from 'chroma-js';

function Weather() {
  const [tempTexture, setTempTexture] = useState(null);
  const fallbackTexture = useLoader(TextureLoader, '/images/earth2.jpg');

  useEffect(() => {
    const generateTemperatureTexture = async () => {
      const res = await fetch('http://localhost:8000/api/weather/');
      const json = await res.json();
      const grid = json.data;
  
      // Dynamically derive width and height from the data
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
        '#4200ff', '#0061ff', '#00d5ff', '#90eb9d',
        '#ffffbf', '#f9d057', '#f29e2e', '#e76818', '#d7191c'
      ]).domain([tempMin, -20, 0, 15, 20, 23, 25, 30, tempMax]);
  
      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          const i = (y * width + x) * 4;
          const temp = grid[y][x];
  
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
      tex.needsUpdate = true;
      setTempTexture(tex);
    };
  
    generateTemperatureTexture();
  }, []);
  

  return (
    <mesh>
      <sphereGeometry args={[2, 51.5, 32.5]} />
      <meshStandardMaterial map={tempTexture || fallbackTexture} />
    </mesh>
  );
}

export default Weather;
