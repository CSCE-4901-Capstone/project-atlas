import { useEffect, useState, useRef, useMemo } from 'react';
import { TextureLoader, Matrix4, BoxGeometry, Object3D } from 'three';
import Loading from 'src/components/builders/Loading';
import * as BufferGeometryUtils from 'three/examples/jsm/utils/BufferGeometryUtils.js';
import convertObjectsToMultiPointGeoJSON from 'src/utils/convertObjectsToMultiPointGeoJSON';
import convertGeoJSONToSphereCoordinates from 'src/utils/convertGeoJSONToSphereCoordinates';
import tranformationHackUtility from 'src/utils/transformationHackUtility';
import api_conn from 'src/utils/api';

function Flights({ radius }) {
  const [data, setData] = useState(null)
    // Pull data from json file
    useEffect(() => {
      async function fetchData() {
        await api_conn.get('/api/flights')
          .then(response => response.data)
          .then(data => {
            console.log(data);
            setData(data)
          })
          .catch(error => console.error('Error fetching json file:', error));
        }

      fetchData();
    }, [radius]); 
return (
        <>
          {data ? <BuildFlights data={data} radius={radius}/> : <Loading />}
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
    let rawPoints = sphereCoordinates['output_coordinate_array'];
    let points = tranformationHackUtility(rawPoints);

    let geometries = [];

    points.forEach(([x, y, z], i) => {
      const geometry = new BoxGeometry(0.015, 0.015, 0.000001);

      // Move geometry to position
      const translationMatrix = new Matrix4().makeTranslation(x, y, z);

      // Make object point at center of globe (Only back texture will be seen)
      const tempObject = new Object3D();
      tempObject.position.set(x, y, z);
      tempObject.lookAt(0,0,0);
      const lookAtMatrix = new Matrix4().makeRotationFromEuler(tempObject.rotation);

      // Make plane face correct direction
      const dirDeg = data[i].direction;
      const dirRad = (dirDeg * Math.PI) / 180;
      const zRotationMatrix = new Matrix4().makeRotationZ(dirRad);

      // Combine all transforms
      const finalMatrix = new Matrix4()
        .multiplyMatrices(translationMatrix, lookAtMatrix)
        .multiply(zRotationMatrix);

      geometry.applyMatrix4(finalMatrix);
      geometries.push(geometry);
    });


      return BufferGeometryUtils.mergeGeometries(geometries, false);
  }, [data, radius]);

  return mergedGeometry ? (
    <mesh ref={groupRef}>
      <primitive object={mergedGeometry} attach="geometry" />
      <meshStandardMaterial map={texture} transparent={true} depthWrite={false} />
    </mesh>
  ) : null;
}

export default Flights;
