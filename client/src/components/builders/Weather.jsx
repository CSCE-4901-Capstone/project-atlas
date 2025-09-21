import { useEffect, useState, useRef } from 'react';
import { useLoader } from '@react-three/fiber';
import { TextureLoader, CanvasTexture, LinearFilter } from 'three';
import chroma from 'chroma-js';

function Weather({ radius, refreshTrigger }) {
  const [tempTexture, setTempTexture] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const fallbackTexture = useLoader(TextureLoader, '/images/earth2.jpg');
  
  const isInitialMount = useRef(true);

  useEffect(() => {
    const generateTemperatureTexture = async (forceRefresh) => {
      setIsLoading(true);
      const url = `http://localhost:8000/api/weather/${forceRefresh ? '?refresh=true' : ''}`;
      
      try {
        const res = await fetch(url);
        const json = await res.json();
        const grid = json.data;

        const height = grid.length;
        const width = grid[0]?.length || 0;

        if (width === 0 || height === 0) {
          console.error("Weather data grid is empty.");
          setIsLoading(false);
          return;
        }

        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        const imageData = ctx.createImageData(width, height);

        const tempMin = -50;
        const tempMax = 40;

        const scale = chroma.scale([
          '#00008B', '#071996', '#0E32A2', '#154AAD', '#1C63B9', '#237BC4', '#2A94D0', '#31ACDC', '#38C5E7', '#40E0D0', '#58D3B8', '#71C6A1', '#89B989', '#A2AC72', '#BA9F5A', '#D39243', '#EB852B', '#FF7814', '#FF690A', '#FF6600'

        ]).domain([tempMin, -45.26, -40.53, -35.79, -31.05, -26.32, -21.58, -16.84, -12.11, -7.37, -2.63, 2.11, 6.84, 11.58, 16.32, 21.05, 25.79, 30.53, 35.26, tempMax]);

        for (let y = 0; y < height; y++) {
          const flippedY = height - 1 - y;
          for (let x = 0; x < width; x++) {
            const i = (y * width + x) * 4;
            const temp = grid[flippedY][x];

            if (temp !== null && temp !== undefined) {
              const [r, g, b] = scale(temp).rgb();
              imageData.data[i] = r;
              imageData.data[i + 1] = g;
              imageData.data[i + 2] = b;
              imageData.data[i + 3] = 170;
            } else {
              imageData.data[i + 3] = 0;
            }
          }
        }

        ctx.putImageData(imageData, 0, 0);
        const tex = new CanvasTexture(canvas);
        tex.minFilter = LinearFilter;
        tex.magFilter = LinearFilter;
        tex.needsUpdate = true;
        setTempTexture(tex);

      } catch (error) {
        console.error("Failed to generate temperature texture:", error);
      } finally {
        setIsLoading(false);
      }
    };

    const isRefresh = !isInitialMount.current;
    generateTemperatureTexture(isRefresh);
    
    isInitialMount.current = false;

  }, [refreshTrigger]);

  return (
    <>
      <mesh>
        <sphereGeometry args={[radius, 64, 32]} />
        <meshStandardMaterial map={fallbackTexture} />
      </mesh>
      {tempTexture && (
        <mesh>
          <sphereGeometry args={[radius + 0.01, 64, 32]} />
          <meshStandardMaterial 
            map={tempTexture}
            transparent={true}
          />
        </mesh>
      )}
    </>
  );
}

export default Weather;
