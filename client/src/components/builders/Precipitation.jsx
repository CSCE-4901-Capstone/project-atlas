import { useEffect, useState, useRef } from 'react';
import { useLoader } from '@react-three/fiber';
import { TextureLoader, CanvasTexture, LinearFilter } from 'three';
import chroma from 'chroma-js';
import api_conn from 'src/utils/api';

const layerConfigs = {
  Precipitation: {
    url: '/api/precipitation/',
    min: 0,
    max: 10, 
    scale: chroma.scale([
        '#00FF00', 
        '#FFFF00', 
        '#FF0000', 
        '#E839A4'  
    ]).domain([0.1, 3, 6, 10]), 
    alpha: 200, 
    type: 'color', 
  },
};

function Precipitation({ radius, refreshTrigger }) {
  const layerType = 'Precipitation'; 
  console.log(`Precipitation component rendered with layerType: ${layerType}`); 
  const [dataTexture, setDataTexture] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const fallbackTexture = useLoader(TextureLoader, '/images/earth2.jpg');
  
  const isInitialMount = useRef(true);
  const canvasRef = useRef(document.createElement('canvas'));

  useEffect(() => {
    const generateDataTexture = async (forceRefresh) => {
      setIsLoading(true);
      const config = layerConfigs[layerType];
      
      let urlPath = config.url;

      if (forceRefresh) {
        const cacheBuster = Date.now();
        urlPath = `${config.url}?cb=${cacheBuster}`;
        console.log(`Data refresh triggered for ${layerType}.`);
      }
      
      try {
        const response = await api_conn.get(urlPath, {
          headers: {
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Expires': '0'
          }
        });

        const json = response.data;
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

            if (value !== null && value !== undefined && value > config.min) {
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

export default Precipitation;
