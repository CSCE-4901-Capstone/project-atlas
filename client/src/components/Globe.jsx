import { useEffect, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
//import Movement from 'src/components/Movement'

function Globe() {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  })

  function handleResize() {
    setWindowSize({
      width: window.innerWidth,
      height: window.innerHeight
    });
  }

  useEffect(() => {
    window.addEventListener('resize', handleResize)
  }, [])

  return (
    <Canvas
      style={{ width: windowSize.width, height: windowSize.height}}
    >

      <OrbitControls /> 
      <mesh>
          <boxGeometry args={[2, 2, 2]} />
          <meshPhongMaterial />
      </mesh>
    </Canvas>
  )
}

export default Globe;
