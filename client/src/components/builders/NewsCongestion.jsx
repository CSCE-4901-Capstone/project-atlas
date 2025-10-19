import { useEffect, useState, useRef, useMemo } from 'react';
import { TextureLoader, Matrix4, BoxGeometry, Object3D, PlaneGeometry, MeshBasicMaterial, Mesh } from 'three';
import * as BufferGeometryUtils from 'three/examples/jsm/utils/BufferGeometryUtils.js';
import convertObjectsToMultiPointGeoJSON from 'src/utils/convertObjectsToMultiPointGeoJSON';
import convertGeoJSONToSphereCoordinates from 'src/utils/convertGeoJSONToSphereCoordinates';
import Error from 'src/components/builders/Error';
import api_conn from 'src/utils/api';

function NewsPopulate({ radius, visible }) {       //function used to load in articles for the countries
  const [data, setData] = useState(null)
    // Pull data from NewsAPI
    useEffect(() => {
      async function fetchData() {
        await api_conn.get('/api/NewsCongestion')       //refer to correct view after referencing urls.py
          .then(response => response.data)
          .then(data => {
            console.log(data);
            setData(data)
          })
          .catch(error => console.error('Error fetching json file:', error));
        }

      fetchData();
    }, [radius]); 

  if (!visible) return null;
  if (data && data.length === 0) return <Error />;
return (                        //build out the heatmap based on the fetched news points
        <>
          {data ? <BuildHeatmap data={data} radius={radius}/> : null}     
        </>
      );
}

function BuildHeatmap({ data, radius }) {
  const groupRef = useRef();

  const texture = new TextureLoader().load('/assets/ArticlePoint.jpg');       //populate the image for a news Point on the globe

  const mergedGeometry = useMemo(() => {

    if (!data || !Array.isArray(data)) return null;
    console.log(data);
    

    // Extract coordinate data
    let json = convertObjectsToMultiPointGeoJSON("Congestion", data);
    let sphereCoordinates = convertGeoJSONToSphereCoordinates(json, radius)
    let points = sphereCoordinates['output_coordinate_array'];


    /*Do something here to build out the hover and click on image function*/

   const geometries = [];


    points.forEach(([x, y, z], i) => {
      //const geometry = new PlaneGeometry(0.005, 0.005, 1, 1);     //originally was box geometry
      /*//if doesnt work use the one below
      ///      const geometry = new BoxGeometry(0.005, 0.005, 0.000001);     //originally was box geometry


      // Move geometry to position
      const translationMatrix = new Matrix4().makeTranslation(x, y, z);
      geometry.applyMatrix4(finalMatrix);
      geometries.push(geometry);*/

      const geometry = new BoxGeometry(0.05, 0.05, 0.000001);

      // Move geometry to position
      const translationMatrix = new Matrix4().makeTranslation(x, y, z);

      // Make object point at center of globe (Only back texture will be seen)
      const tempObject = new Object3D();
      tempObject.position.set(x, y, z);
      tempObject.lookAt(0,0,0);
      const lookAtMatrix = new Matrix4().makeRotationFromEuler(tempObject.rotation);

      const zRotationMatrix = new Matrix4().makeRotationZ(0);

      // Combine all transforms
      const finalMatrix = new Matrix4()
        .multiplyMatrices(translationMatrix, lookAtMatrix)
        .multiply(zRotationMatrix);

      geometry.applyMatrix4(finalMatrix);
      geometries.push(geometry);
    });

      console.log(geometries);
      try{
        return BufferGeometryUtils.mergeGeometries(geometries, false);
      } catch(e){
        console.error("Failed to load heatmap.");
      }
      if(geometries.length > 0){
        return BufferGeometryUtils.mergeGeometries(geometries, false);
      }
  }, [data, radius]);

  useEffect(() => {
     if (groupRef.current) {
      groupRef.current.rotation.x = -Math.PI * 0.5; // Quick hack to fix rotation
     }
  }, [])

  const material = new MeshBasicMaterial({color: 0xff00ff});

  return mergedGeometry ? (
    <mesh ref={groupRef} material={material}>
      <primitive object={mergedGeometry} attach="geometry" />
    </mesh>
  ) : null;
}

export default NewsPopulate;
