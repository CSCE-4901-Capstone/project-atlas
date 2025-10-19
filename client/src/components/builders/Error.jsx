import { Html } from '@react-three/drei';

function Error() {

  return (
    <Html center>
      <div style={{
        width:'500px',
        display: 'flex',
        justifyContent: 'center'
      }}>
        <img
            src="images/error.png"
            alt="loading"
            style={{
              pointerEvents: "none",                 
              userSelect: "none",        
              draggable: false
            }}
         />
      </div>
      <h1 style ={{
        color: 'white',
        width: '500px'
      }}> An Error has occured with the API </h1>
    </Html>
  )
}

export default Error;

