import { useEffect, useState, useRef, useMemo } from 'react';
import { TextureLoader, Matrix4, BoxGeometry, Object3D } from 'three';
import Loading from 'src/components/builders/Loading';
import * as BufferGeometryUtils from 'three/examples/jsm/utils/BufferGeometryUtils.js';
import convertObjectsToMultiPointGeoJSON from 'src/utils/convertObjectsToMultiPointGeoJSON';
import convertGeoJSONToSphereCoordinates from 'src/utils/convertGeoJSONToSphereCoordinates';
import tranformationHackUtility from 'src/utils/transformationHackUtility';
import api_conn from 'src/utils/api';

function Disasters({ radius }) {
  const [data, setData] = useState(null)
    // Pull data from json file
    useEffect(() => {
      async function fetchData() {
        await api_conn.get('/api/disaster')
          .then(response => response.data)
          .then(data => {
            setData(data)
          })
          .catch(error => console.error('Error fetching json file:', error));
        }

      fetchData();
    }, [radius]); 
return (
        <>
          {data ? <BuildDisasters data={data} radius={radius}/> : <Loading />}
        </>
      );
}

function BuildDisasters({ data, radius }) {
  // Group disaster types to avoid any performance issues
  const groupRef = useRef();

  // Returns an array of grouped disaster types
  const mergedGroups = useMemo(() => {
    const loader = new TextureLoader();

    const textures = {
      wildfires: loader.load('/images/wildfire.png'),
      severeStorms: loader.load('/images/storm.png'),
      volcanoes: loader.load('/images/volcano.png'),
      seaLakeIce: loader.load('/images/ice.png'),
    };

    // Creates disaster types based on any new disaster types introduced by the api
    const grouped = {};
    for (const disaster of data) {
      if (!grouped[disaster.type]) grouped[disaster.type] = [];
      grouped[disaster.type].push(disaster);
    }
    console.log(grouped)

    // Build geometries for each group
    const groups = Object.entries(grouped).map(([type, disasters]) => {
      const geometries = [];
      const json = convertObjectsToMultiPointGeoJSON("Disasters", disasters);
      const sphereCoords = convertGeoJSONToSphereCoordinates(json, radius);
      const rawPoints = sphereCoords.output_coordinate_array;
      const points = tranformationHackUtility(rawPoints);

      points.forEach(([x, y, z]) => {
        const geometry = new BoxGeometry(0.03, 0.03, 0.000001);

        // Sets the geometry position
        const translationMatrix = new Matrix4().makeTranslation(x, y, z);

        // Creates the geometry and makes it face the center
        const tempObj = new Object3D();
        tempObj.position.set(x, y, z);
        tempObj.lookAt(0, 0, 0);

        const lookAtMatrix = new Matrix4().makeRotationFromEuler(tempObj.rotation);

        // Applys matrices
        geometry.applyMatrix4(new Matrix4().multiplyMatrices(translationMatrix, lookAtMatrix));
        geometries.push(geometry);
      });

      // Merges geometries for effeciency
      const merged = BufferGeometryUtils.mergeGeometries(geometries, false);

      return (
        <mesh key={type} geometry={merged}>
          <meshStandardMaterial
            map={textures[type] || null}
            transparent
            depthWrite={false}
          />
        </mesh>
      );
    });

    return groups;
  }, [data, radius]);

  return <group ref={groupRef}>{mergedGroups}</group>;
}

export default Disasters;
