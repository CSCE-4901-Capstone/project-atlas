import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
//import { Movement } from 'src/components/Movement'

function Globe() {
  
  return (
    <Canvas
      style={{ width: window.innerWidth, height: window.innerHeight}}
    >

      //<OrbitControls enableZoom={true} />
      
      <mesh>
          <boxGeometry args={[2, 2, 2]} />
          <meshPhongMaterial />
      </mesh>
    </Canvas>
  )
}

export default Globe;
