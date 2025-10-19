import { useMemo, useEffect, useState, useRef } from 'react';
import { CanvasTexture, LinearFilter } from 'three';
import chroma from 'chroma-js';
import Loading from 'src/components/builders/Loading';
import fetchData from 'src/utils/fetchData';

const scale = chroma.scale([
      '#8A2BE2', '#783CD2', '#664DC2', '#545CB1', '#4169E1', '#6983E1', '#91A1E1', '#B9BEE0', '#E1DCE0', '#F0F0D2', '#FFFFE0', '#FFF0AC', '#FFDB74', '#FFC73C', '#FFB304', '#FFA500', '#FF7B00', '#FF5200', '#FF2800', '#FF0000'
    ]).domain([-50, -35.79, -31.58, -27.37, -23.16, -18.95, -14.74, -10.53, -6.32, -2.11, 2.11, 6.32, 10.53, 14.74, 18.95, 23.16, 27.37, 31.58, 35.79, 40]);
const alpha = 195;
const min = -50;

function Weather({ radius, visible }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    let mounted = true;

    fetchData('/api/weather').then((res) => {
      if (mounted) setData(res.data);
    });

    return () => { mounted = false };
  }, [radius]);

  if (!visible) return null;

  return data ? <BuildWeather data={data} radius={radius} /> : <Loading />;
}

function BuildWeather ({ data, radius }) {
  const canvasRef = useRef(document.createElement('canvas'));

  const dataTexture = useMemo(() => {
    const grid = data;

    const height = grid.length;
    const width = grid[0]?.length || 0;


    if (width === 0 || height === 0) {
      console.error(`data grid is empty.`);
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

        if (value !== null && value !== undefined && value >= min) {
          const [r, g, b] = scale(value).rgb();
          imageData.data[i] = r;
          imageData.data[i + 1] = g;
          imageData.data[i + 2] = b;
          imageData.data[i + 3] = alpha;
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
    return tex
  }, [data])

  return (
    <>
      <mesh>
        <sphereGeometry args={[radius + 0.01, 64, 32]} />
        <meshStandardMaterial 
          map={dataTexture}
          transparent={true}
          depthWrite={true} 
        />
      </mesh>
   </>
  )

}

export default Weather;
