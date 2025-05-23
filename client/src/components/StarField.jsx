import { useEffect } from 'react'
import { useThree } from '@react-three/fiber'
import { Vector3, Color, FogExp2 } from 'three'

function StarField({ numStars }) {
  const { scene } = useThree()
  const positions = [];
  const colors = [];
     
  for (let i = 0; i < numStars; i++) {
    let pos = randomPoint();
    let col = new Color(`hsl(60%, 20%, {Math.random()})`)  

    positions.push(pos.x, pos.y, pos.z)
    colors.push(col.r, col.g, col.b)
  }

  // Add some fog to the scene to make the stars look a bit more realistic
  useEffect(() => {
    scene.fog = new FogExp2('black', 0.03);
  }, [scene])

  return (
    <points>
      <bufferGeometry>
        <bufferAttribute
          attach='attributes-position'
          array={new Float32Array(positions)}
          count={positions.length / 3}
          itemSize={3} 
        />
        <bufferAttribute
          attach='attributes-color'
          array={new Float32Array(colors)}
          count={positions.length / 3}
          itemSize={3} 
        />
      </bufferGeometry>
      <pointsMaterial size={0.2} vertexColors fog={true}/>
    </points>

  )
}

// Select a random point for the radius, longitude and lattitude
function randomPoint() {
  const radius = Math.random() * 20 + 20; // Pick a radius between 20 and 40
  const longitude = 2 * Math.PI * Math.random();
  const latitude = Math.acos(2 * Math.random() - 1);

  const x = radius * Math.sin(latitude) * Math.cos(longitude);
  const y = radius * Math.sin(latitude) * Math.sin(longitude);
  const z = radius * Math.cos(latitude);

  return new Vector3(x, y, z);
}

export default StarField;
