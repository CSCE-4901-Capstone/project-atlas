import { useState, useRef } from 'react';
import { useThree, useFrame } from '@react-three/fiber';

function Movement() {
  const { camera } = useThree();
  const [isDragging, setIsDragging] = useState(false);
  const lastMousePos = useRef({x: 0, y: 0});
  const rotation = useRef({x: 0, y: 0});

  const handleMouseDown = (event) => {
    lastMousePos.current = {x: event.clientX, y: event.clientY};
    setIsDragging(true);
  }

  const handleMouseUp = (event) => {
    setIsDragging(false);
  }

  const handleMouseMove = (event) => {
    if (!isDragging) return;

    const deltaX = (event.clientX - lastMousePos.current.x) * 0.005; // Adjust sensitivity
    const deltaY = (event.clientY - lastMousePos.current.y) * 0.005;

    rotation.current.x += deltaX;
    rotation.current.y = Math.min(Math.max(rotation.current.y + deltaY, -1.5), 1.5); // Limit vertical rotation

    lastMousePos.current = { x: event.clientX, y: event.clientY };

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
    />
  )
  
}

export default Movement;
