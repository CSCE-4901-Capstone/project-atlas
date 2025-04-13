import { useEffect, useState, useRef, useMemo } from 'react';
import { TextureLoader, Matrix4, BoxGeometry, Object3D } from 'three';
import * as BufferGeometryUtils from 'three/examples/jsm/utils/BufferGeometryUtils.js';
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

  const texture = new TextureLoader().load('/images/flight.png');

  const mergedGeometry = useMemo(() => {
    // Extract coordinate data
    let json = convertObjectsToMultiPointGeoJSON("Flights", data);
    let sphereCoordinates = convertGeoJSONToSphereCoordinates(json, radius)
    let points = sphereCoordinates['output_coordinate_array'];

    let geometries = [];

    console.log(points.length)
    console.log(data.length)
    points.forEach(([x, y, z]) => {
      const geometry = new BoxGeometry(0.02, 0.02, 0.002);

      // Create a matrix to translate to the position
      const translationMatrix = new Matrix4().makeTranslation(x, y, z);

      // Create a temporary object to use lookAt and get rotation position
      const tempObject = new Object3D();
      tempObject.position.set(x, y, z);
      tempObject.lookAt(0, 0, 0);
      const rotationMatrix = new Matrix4().makeRotationFromEuler(tempObject.rotation);

      // Combine translation and rotation
      const finalMatrix = new Matrix4().multiplyMatrices(translationMatrix, rotationMatrix);

      geometry.applyMatrix4(finalMatrix);
      geometries.push(geometry);
    });


      return BufferGeometryUtils.mergeGeometries(geometries, false);
  }, [data, radius]);

  useEffect(() => {
     if (groupRef.current) {
      groupRef.current.rotation.x = -Math.PI * 0.5; // Quick hack to fix rotation
     }
  }, [])

  return mergedGeometry ? (
    <mesh ref={groupRef}>
      <primitive object={mergedGeometry} attach="geometry" />
      <meshBasicMaterial map={texture} transparent />
    </mesh>
  ) : null;
}

export default Flights;
