import { useEffect, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import StarField from 'src/components/StarField';
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
      style={{ width: windowSize.width, height: windowSize.height, background: 'black'}}
    >
      <ambientLight intensity={2} />
      <StarField numStars={500}/>
      <OrbitControls />
      <mesh>
          <sphereGeometry args={[2, 51, 32]} />
          <meshStandardMaterial color={'blue'} />
      </mesh>
    </Canvas>
  )
}

export default Globe;
