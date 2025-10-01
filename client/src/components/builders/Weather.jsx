import { useEffect, useState, useRef } from 'react';
import { useLoader } from '@react-three/fiber';
import { TextureLoader, CanvasTexture, LinearFilter } from 'three';
import chroma from 'chroma-js';

const precipitationIcons = {
  Rain: '/images/raindrop.png',
  HeavyRain: '/images/lightning.png',
  Snow: '/images/snowflake.png',
};

const layerConfigs = {
  Temperature: {
    url: 'http://localhost:8000/api/weather/',
    min: -50,
    max: 40,
    scale: chroma.scale([
      '#8A2BE2', '#783CD2', '#664DC2', '#545CB1', '#4169E1', '#6983E1', '#91A1E1', '#B9BEE0', '#E1DCE0', '#F0F0D2', '#FFFFE0', '#FFF0AC', '#FFDB74', '#FFC73C', '#FFB304', '#FFA500', '#FF7B00', '#FF5200', '#FF2800', '#FF0000'
    ]).domain([-50, -35.79, -31.58, -27.37, -23.16, -18.95, -14.74, -10.53, -6.32, -2.11, 2.11, 6.32, 10.53, 14.74, 18.95, 23.16, 27.37, 31.58, 35.79, 40]),
    alpha: 195, //Opacity: 76% 
    type: 'color', 
  },
  Precipitation: {
    url: 'http://localhost:8000/api/precipitation/',
    min: 0.1, //Don't show transparent for 0mm
    max: 50,  //Max precipitation in mm/hr for the scale
    alpha: 220, //Opacity: 85%
    type: 'icon', 
    iconMap: [
      {max: 1, icon: precipitationIcons.Rain},         // 0.1 - .1 mm/hr (Light/Moderate Rain)
      {max: 15, icon: precipitationIcons.HeavyRain},   // .1 - 13 mm/hr (Heavy Rain/Storms)
      {max: Infinity, icon: precipitationIcons.Snow},  // > 13 mm/hr (Treating highest as 'snow' or just a very severe indicator)
    ],
  },
};

function Weather({ radius, layerType = 'Weather', refreshTrigger }) {
  console.log(`Weather component rendered with layerType: ${layerType}`); 
  const [dataTexture, setDataTexture] = useState(null);
  const [iconTextures, setIconTextures] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const fallbackTexture = useLoader(TextureLoader, '/images/earth2.jpg');
  
  const isInitialMount = useRef(true);
  const canvasRef = useRef(document.createElement('canvas'));

  useEffect(() => {
    if (layerType === 'Precipitation') {
      const config = layerConfigs.Precipitation;
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
    } else {
      setIconTextures({});
    }
  }, [layerType, refreshTrigger]);


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
        
        if (config.type === 'color') {
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
                imageData.data[i + 3] = config.alpha; //Use alpha from config
              } else {
                imageData.data[i + 3] = 0; //Transparent
              }
            }
          }
          ctx.putImageData(imageData, 0, 0);

        } else if (config.type === 'icon') {
          ctx.clearRect(0, 0, width, height);
          
          ctx.save(); 
          ctx.translate(0, height);
          ctx.scale(1, -1); 
          
          const iconSize = 4;

          for (let y = 0; y < height; y += iconSize) { 
            const dataY = Math.floor(y);

            for (let x = 0; x < width; x += iconSize) { 
              
              const dataX = Math.floor(x);
              
              if (dataY < height && dataX < width) {
                const value = grid[dataY][dataX];
                
                if (value !== null && value !== undefined && value >= config.min) {
                  const iconConfig = config.iconMap.find(item => value <= item.max);
                  
                  if (iconConfig) {
                    const iconImage = iconTextures[iconConfig.icon];
                    
                    if (iconImage) {
                      ctx.drawImage(
                        iconImage, 
                        x, 
                        y, 
                        iconSize, 
                        iconSize
                      );
                    }
                  }
                }
              }
            }
          }
          ctx.restore(); 
        }

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
    
    const isReadyToRun = layerConfigs[layerType]?.type === 'color' || (layerConfigs[layerType]?.type === 'icon' && Object.keys(iconTextures).length > 0);
                         
    if (isReadyToRun) {
      generateDataTexture(isRefresh);
    }
    
    isInitialMount.current = false;

  }, [layerType, refreshTrigger, iconTextures]);

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
            depthWrite={layerConfigs[layerType]?.type === 'icon' ? false : true} 
          />
        </mesh>
      )}
    </>
  );
}

export default Weather;
