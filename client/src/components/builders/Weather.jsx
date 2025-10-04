import { useEffect, useState, useRef } from 'react';
import { useLoader } from '@react-three/fiber';
import { TextureLoader, CanvasTexture, LinearFilter } from 'three';
import chroma from 'chroma-js';

const layerConfigs = {
  Temperature: {
    url: 'http://localhost:8000/api/weather/',
    min: -50,
    max: 40,
    scale: chroma.scale([
      '#8A2BE2', '#783CD2', '#664DC2', '#545CB1', '#4169E1', '#6983E1', '#91A1E1', '#B9BEE0', '#E1DCE0', '#F0F0D2', '#FFFFE0', '#FFF0AC', '#FFDB74', '#FFC73C', '#FFB304', '#FFA500', '#FF7B00', '#FF5200', '#FF2800', '#FF0000'
    ]).domain([-50, -35.79, -31.58, -27.37, -23.16, -18.95, -14.74, -10.53, -6.32, -2.11, 2.11, 6.32, 10.53, 14.74, 18.95, 23.16, 27.37, 31.58, 35.79, 40]),
    alpha: 195,
    type: 'color', 
  },
};

function Weather({ radius, refreshTrigger }) {
  const layerType = 'Temperature'; 
  console.log(`Weather component rendered with layerType: ${layerType}`); 
  const [dataTexture, setDataTexture] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const fallbackTexture = useLoader(TextureLoader, '/images/earth2.jpg');
  
  const isInitialMount = useRef(true);
  const canvasRef = useRef(document.createElement('canvas'));

  useEffect(() => {
    const generateDataTexture = async (forceRefresh) => {
      setIsLoading(true);
      const config = layerConfigs[layerType];
      const url = `${config.url}${forceRefresh ? '?refresh=true' : ''}`;
      
      try {
        const res = await fetch(url);
        const json = await res.json();
        const grid = json.data;

        const height = grid.length;
        const width = grid[0]?.length || 0;

        if (width === 0 || height === 0) {
          console.error(`${layerType} data grid is empty.`);
          setIsLoading(false);
          return;
        }

        const canvas = canvasRef.current;
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        
        const imageData = ctx.createImageData(width, height);

        for (let y = 0; y < height; y++) {
          const flippedY = height - 1 - y;
          for (let x = 0; x < width; x++) {
            const i = (y * width + x) * 4;
            const value = grid[flippedY][x];

            if (value !== null && value !== undefined && value >= config.min) {
              const [r, g, b] = config.scale(value).rgb();
              imageData.data[i] = r;
              imageData.data[i + 1] = g;
              imageData.data[i + 2] = b;
              imageData.data[i + 3] = config.alpha;
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
        setDataTexture(tex);

      } catch (error) {
        console.error(`Failed to generate ${layerType} texture:`, error);
      } finally {
        setIsLoading(false);
      }
    };

    const isRefresh = !isInitialMount.current;
                         
    generateDataTexture(isRefresh);
    
    isInitialMount.current = false;

  }, [refreshTrigger]);

  return (
    <>
      <mesh>
        <sphereGeometry args={[radius, 64, 32]} />
        <meshStandardMaterial map={fallbackTexture} />
      </mesh>
      {dataTexture && (
        <mesh>
          <sphereGeometry args={[radius + 0.01, 64, 32]} />
          <meshStandardMaterial 
            map={dataTexture}
            transparent={true}
            depthWrite={true} 
          />
        </mesh>
      )}
    </>
  );
}

export default Weather;
