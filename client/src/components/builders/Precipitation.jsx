import { useEffect, useState, useRef } from 'react';
import { useLoader } from '@react-three/fiber';
import { TextureLoader, CanvasTexture, LinearFilter, LinearMipmapLinearFilter } from 'three';

const precipitationIcons = {
  Rain: '/images/raindrop.png',
  HeavyRain: '/images/lightning.png',
  Snow: '/images/snowflake.png',
};

const layerConfig = {
    url: 'http://localhost:8000/api/precipitation/',
    min: 0.1,
    max: 50,
    alpha: 220,
    type: 'icon', 
    iconMap: [
      {max: 1, icon: precipitationIcons.Rain},
      {max: 15, icon: precipitationIcons.HeavyRain},
      {max: Infinity, icon: precipitationIcons.Snow},
    ],
};

function Precipitation({ radius, refreshTrigger }) {
  const layerType = 'Precipitation';
  console.log(`Precipitation component rendered`); 
  const [dataTexture, setDataTexture] = useState(null);
  const [iconTextures, setIconTextures] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  
  const isInitialMount = useRef(true);
  const canvasRef = useRef(document.createElement('canvas'));

  useEffect(() => {
    const config = layerConfig;
    const loader = new TextureLoader();
    const newIconTextures = {};
    const uniqueIcons = [...new Set(config.iconMap.map(item => item.icon))];
    
    const loadPromises = uniqueIcons.map(url => new Promise((resolve, reject) => {
      loader.load(url, (texture) => {
        newIconTextures[url] = texture.image;
        resolve();
      }, undefined, reject);
    }));

    Promise.all(loadPromises)
      .then(() => setIconTextures(newIconTextures))
      .catch(error => console.error("Failed to load precipitation icons:", error));
  }, []);

  useEffect(() => {
    const generateDataTexture = async (forceRefresh) => {
      setIsLoading(true);
      const config = layerConfig;
      const url = `${config.url}${forceRefresh ? '?refresh=true' : ''}`;
      
      if (Object.keys(iconTextures).length === 0) return;

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
        
        const scaleFactor = 16; 
        const highResCanvas = document.createElement('canvas');
        highResCanvas.width = width * scaleFactor;
        highResCanvas.height = height * scaleFactor;
        const highResCtx = highResCanvas.getContext('2d');

        highResCtx.clearRect(0, 0, highResCanvas.width, highResCanvas.height);
        highResCtx.imageSmoothingEnabled = true;
        
        highResCtx.save(); 
        
        const baseIconStep = 4;
        const iconSize = baseIconStep * scaleFactor; 

        const poleExclusionZone = Math.floor(height * 0.05); 

        for (let y = 0; y < height; y += baseIconStep) { 
          
          if (y < poleExclusionZone || y > (height - 1 - poleExclusionZone)) {
              continue; 
          }

          const dataY = height - 1 - Math.floor(y);

          for (let x = 0; x < width; x += baseIconStep) { 
            
            const dataX = Math.floor(x);
            
            if (dataY >= 0 && dataX < width) {
              const value = grid[dataY][dataX];
              
              if (value !== null && value !== undefined && value >= config.min) {
                const iconConfig = config.iconMap.find(item => value <= item.max);
                
                if (iconConfig) {
                  const iconImage = iconTextures[iconConfig.icon];
                  
                  if (iconImage) {
                    highResCtx.drawImage(
                      iconImage, 
                      x * scaleFactor, 
                      y * scaleFactor, 
                      iconSize, 
                      iconSize
                    );
                  }
                }
              }
            }
          }
        }
        highResCtx.restore();
        
        ctx.clearRect(0, 0, width, height);
        ctx.drawImage(highResCanvas, 0, 0, width, height);

        const tex = new CanvasTexture(canvas);
        
        tex.minFilter = LinearMipmapLinearFilter;
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
                         
    if (Object.keys(iconTextures).length > 0) {
      generateDataTexture(isRefresh);
    }
    
    isInitialMount.current = false;

  }, [refreshTrigger, iconTextures]);

  return (
    dataTexture && (
      <mesh>
        <sphereGeometry args={[radius + 0.01, 64, 32]} />
        <meshStandardMaterial 
          map={dataTexture}
          transparent={true}
          depthWrite={false} 
        />
      </mesh>
    )
  );
}

export default Precipitation;