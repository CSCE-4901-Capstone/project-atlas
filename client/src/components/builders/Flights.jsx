import { useEffect, useState, useRef, useMemo } from 'react';
import { TextureLoader, Matrix4, PlaneGeometry, MeshBasicMaterial } from 'three';
import { Line } from '@react-three/drei';
import convertObjectsToMultiPointGeoJSON from 'src/utils/convertObjectsToMultiPointGeoJSON';
import convertGeoJSONToSphereCoordinates from 'src/utils/convertGeoJSONToSphereCoordinates';
import api_conn from 'src/utils/api';

function Flights({ radius }) {
  const [data, setData] = useState(null)
    // Pull data from json file
    useEffect(() => {
      async function fetchData() {
        await api_conn.get('/api/flights') .then(response => response.data) .then(data => {
            console.log(data);
            setData(data)
          })
          .catch(error => console.error('Error fetching json file:', error));
        }

      fetchData();
    }, [radius]); 
return (
        <>
          {data ? <BuildFlights data={data} radius={radius}/> : null}
        </>
      );
}

function BuildFlights({ data, radius }) {
  const groupRef = useRef();

  let json = convertObjectsToMultiPointGeoJSON("Flights", data);
  let sphereCoordinates = convertGeoJSONToSphereCoordinates(json, radius)
  let points = sphereCoordinates['output_coordinate_array'];

  const texture = new TextureLoader().load('/images/flight.png');

  useEffect(() => {
     if (groupRef.current) {
      groupRef.current.rotation.x = -Math.PI * 0.5; // Quick hack to fix rotation
     }
  }, [])

  return (
    <FlightPoints ref={groupRef} positions={points} texture={texture} />
  )
}

function FlightPoints({ positions, texture }) {
  const meshRef = useRef();

  useEffect(() => {
    if (meshRef.current) {
      const matrix = new Matrix4();
      const positionsArray = new Float32Array(positions.flat());
      const count = positionsArray.length / 3;

      // Set matrix for each instance
      for (let i = 0; i < count; i++) {
        const posX = positionsArray[i * 3];
        const posY = positionsArray[i * 3 + 1];
        const posZ = positionsArray[i * 3 + 2];
        matrix.setPosition(posX, posY, posZ);
        meshRef.current.setMatrixAt(i, matrix);
      }
    }
  }, [positions]);


  return (
    <>
      <instancedMesh ref={meshRef} args={[new PlaneGeometry(0.05, 0.05), new MeshBasicMaterial({ map: texture }), positions.length / 3]}>
        {/* Use planeGeometry for the individual instances */}
      </instancedMesh>
    </>
  );
}


export default Flights;
