import { useEffect, useState } from 'react';
import { useRef } from 'react';
import { Line } from '@react-three/drei';
import convertGeoJSONToSphereCoordinates from 'src/utils/convertGeoJSONToSphereCoordinates';

function Outline({ filename, radius }) {
  const [json, setJson] = useState(null)

  // Pull data from json file
  useEffect(() => {
    fetch(`/json/${filename}`)
      .then(response => response.json())
      .then(json => {
        setJson(json)
      })
      .catch(error => console.error('Error loading the GeoJSON file:', error));
  }, [filename, radius]); 

  return (
    <>
      {json ? <BuildOutline json={json} radius={radius}/> : null}
    </>
  );
}

function BuildOutline({ json, radius }) {
  const groupRef = useRef();
  let sphereCoordinates = convertGeoJSONToSphereCoordinates(json, radius)
  let coordArray = sphereCoordinates['output_coordinate_array'];

  useEffect(() => {
     if (groupRef.current) {
      groupRef.current.rotation.x = -Math.PI * 0.5; // Quick hack to fix rotation
     }
  }, [])

  return (
    <group onClick = {(e) => { console.log(e)}} ref={groupRef}>
      {coordArray.map((line, index) => (
        <Line key={index} points={line} color={'white'} lineWidth={1} />
      ))}
    </group>
  )
}


export default Outline;
