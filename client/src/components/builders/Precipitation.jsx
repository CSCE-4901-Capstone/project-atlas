import { useMemo, useEffect, useState, useRef } from 'react';
import { CanvasTexture, LinearFilter } from 'three';
import chroma from 'chroma-js';
import Loading from 'src/components/builders/Loading';
import fetchData from 'src/utils/fetchData';

const scale = chroma.scale([
        '#00FF00', 
        '#FFFF00', 
        '#FF0000', 
        '#E839A4'  
    ]).domain([0.1, 3, 6, 10])
const alpha = 200;
const min = 0;

function Precipitation({ radius, visible }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    let mounted = true;

    fetchData('/api/precipitation/').then((res) => {
      if (mounted) setData(res.data);
    });

    return () => { mounted = false };
  }, [radius]);

  if (!visible) return null;

  return data ? <BuildPrecipitation data={data} radius={radius} /> : <Loading />;
}

function BuildPrecipitation ({ data, radius }) {
  const canvasRef = useRef(document.createElement('canvas'));

  const dataTexture = useMemo(() => {
    const grid = data;
    console.log(grid)
    console.log('test')

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

export default Precipitation;
