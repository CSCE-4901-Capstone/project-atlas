import { useEffect, useState, useMemo } from 'react';
import { useRef } from 'react';
import { Line } from '@react-three/drei';
import convertGeoJSONToSphereCoordinates from 'src/utils/convertGeoJSONToSphereCoordinates';

function CountryOutline({ filename, radius, color }) {
  const [json, setJson] = useState(null)

  // Pull data from json file
  useEffect(() => {
    fetch(`/json/outlines/${filename}`)
      .then(response => response.json())
      .then(json => {
        setJson(json)
      })
      .catch(error => console.error('Error loading the GeoJSON file:', error));
  }, [filename, radius]); 

  return (
    <>
      {json ? <BuildOutline json={json} radius={radius} color={color}/> : null}
    </>
  );
}

function BuildOutline({ json, radius, color}) {
  const groupRef = useRef();
  const coordArray = useMemo(() => {
    let sphereCoordinates = convertGeoJSONToSphereCoordinates(json, radius);
    return sphereCoordinates['output_coordinate_array']
  }, [json, radius]);

  useEffect(() => {
     if (groupRef.current) {
      groupRef.current.rotation.x = -Math.PI * 0.5; // Quick hack to fix rotation
     }
  }, [])


  return (
    <group onClick = {(e) => { console.log(e)}} ref={groupRef}>
      {coordArray.map((line, index) => (
        <Line key={index} points={line} color={color} lineWidth={1} />
      ))}
    </group>
  )
}


export default CountryOutline;
