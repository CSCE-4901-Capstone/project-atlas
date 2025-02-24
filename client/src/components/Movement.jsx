import { useState, useRef} from 'react';
import { useThree, useFrame } from '@react-three/fiber';

function Movement() {
  const { camera } = useThree();
  const [isDragging, setIsDragging] = useState(false);
  const [lastMousePos, setLastMousePos] = useRef({x: 0, y: 0});
  const [rotation, setRotation] = useRef({x: 0, y: 0});

  const handleMouseDown = (event) => {
    setLastMousePos({x: event.clientX, y: event.clientY});
    setIsDragging(true);
  }

  const handleMouseUp = (event) => {
    setIsDragging(false);
  }

  const handleMouseMove = (event) => {
    if (!isDragging) return;


  }

  useFrame(() => {
    let x = Math.sin(rotation.x)
    let y = Math.sin(rotation.y)
    let z = Math.cos(rotation.x) * Math.cos(rotation.y);
    camera.position(x, y, z);
    camera.lookat(0, 0, 0)
  })



  return (
    <div
    onMouseDown={handleMouseDown}
    onMouseUp={handleMouseUp}
    onMouseMove={handleMouseMove}
    style={{display: 'absolute', width: window.innerWidth, height: window.innerHeight}}
    >
    </div>
  )
  
}

export default Movement;
