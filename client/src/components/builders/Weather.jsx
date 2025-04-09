import { useEffect, useState } from 'react';
import { useLoader } from '@react-three/fiber';
import { TextureLoader, CanvasTexture, LinearMipMapLinearFilter } from 'three';
import { OrbitControls } from '@react-three/drei';
import chroma from 'chroma-js';
import api_conn from 'src/utils/api';

function Weather() {
  const [tempTexture, setTempTexture] = useState(null);
  const fallbackTexture = useLoader(TextureLoader, '/images/earth2.jpg');

  useEffect(() => {
    async function fetchData() {
      await api_conn
        .get('/api/weather-grid/')
        .then(response => response.data)
        .then(data => {
          console.log('Weather Grid:', data);
          generateTexture(data);
        })
        .catch(error => console.error('Error fetching weather data:', error));
    }

    const generateTexture = (json) => {
      const width = json.width;
      const height = json.height;
      const temperatureData = json.data;

      const canvas = document.createElement('canvas');
      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext('2d');
      const imageData = ctx.createImageData(width, height);

      const tempMin = -98;
      const tempMax = 60;
      const scale = chroma.scale([
        '#4200ff', '#0061ff', '#00d5ff', '#a0ddff', '#ffffff',
        '#ffffcc', '#ffff00', '#ff8000', '#ff0000'
      ]).domain([
        tempMin, 0, 15, 21, 23, 25, 30, 40, tempMax
      ]);

      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          const i = (y * width + x) * 4;
          const temp = temperatureData[y][x] ?? tempMin;
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
      tex.needsUpdate = true;
      setTempTexture(tex);
    };

    fetchData();
  }, []);

  return (
    <>
      <ambientLight intensity={1} />
      <OrbitControls makeDefault />
      <mesh>
        <sphereGeometry args={[2, 450, 450]} />
        <meshStandardMaterial
          map={tempTexture || fallbackTexture}
          transparent={true}
          opacity={0.7}
        />
      </mesh>
    </>
  );
}

export default Weather;

