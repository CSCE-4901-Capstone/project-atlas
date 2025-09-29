import { Html } from '@react-three/drei';

function Loading() {

  return (
    <Html center>
      <img
          src="images/loading.svg"
          alt="loading"
          style={{
            opacity: 0.7,
            pointerEvents: "none",                 
            userSelect: "none",        
            draggable: false
          }}
       />
    </Html>
  )
}

export default Loading;

