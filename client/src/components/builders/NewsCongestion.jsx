import { useEffect, useState, useRef, useMemo } from 'react';
import { TextureLoader, Matrix4, BoxGeometry, Object3D, PlaneGeometry, MeshBasicMaterial, Mesh } from 'three';
import * as BufferGeometryUtils from 'three/examples/jsm/utils/BufferGeometryUtils.js';
import convertObjectsToMultiPointGeoJSON from 'src/utils/convertObjectsToMultiPointGeoJSON';
import convertGeoJSONToSphereCoordinates from 'src/utils/convertGeoJSONToSphereCoordinates';
import tranformationHackUtility from 'src/utils/transformationHackUtility';
import { Canvas } from '@react-three/fiber'
import Error from 'src/components/builders/Error';
import api_conn from 'src/utils/api';
import { Html } from '@react-three/drei'                    //for floting link on articles
//import { useFrame } from '@react-three/fiber';              //for animation of rising box geometry


function NewsPopulate({ radius, visible }) {       //function used to load in articles for the countries
  const [data, setData] = useState(null)
  // Pull data from NewsAPI
  useEffect(() => {
    async function fetchData() {
      await api_conn.get('/api/NewsCongestion')       //refer to correct view after referencing urls.py
        .then(response => response.data)
        .then(data => {
          console.log(data);
          setData(data);
        })
        .catch(error => console.error('Error fetching json file:', error));
    }

    fetchData();
  }, [radius]);

  if (!visible) return null;
  if (data && data.length === 0) return <Error />;
  return (                        //build out the heatmap based on the fetched news points
    <>
      {data ? <BuildHeatmap data={data} radius={radius} /> : null}
    </>
  );
}

function BuildHeatmap({ data, radius }) {
  const groupRef = useRef();

  //Reference parameters for the hover and click
  const [hoverIdx, setHoverIdx] = useState(null)   // which point is hovered
  const [hoverPos, setHoverPos] = useState(null)   // world position for tooltip
  const pointsRef = useRef([])                     // stores [x,y,z] for each point
  const dataRef = useRef([])                       // stores original data aligned to points
  const allDataRef = useRef([])                    // all articles recieved
  //end

  const texture = new TextureLoader().load('/images/ArticlePoint.jpg');       //populate the image for a news Point on the globe
  const [selectedGroup, setSelectedGroup] = useState(null);


  const mergedGeometry = useMemo(() => {
    if (!data || !Array.isArray(data)) return null;

    console.log("Incoming data:", data);

    // Flatten 2D array for data organization
    const flatData = data.flat();

    console.log("Flattened data:", flatData);

    //Store all articles separately
    allDataRef.current = flatData;

    //Reset per-geometry data array so it is ready to collect articles per one geometry
    dataRef.current = [];

    // --- Group points by latitude + longitude ---
    const grouped = new Map();
    flatData.forEach(item => {
      //set the key to each item's lat and long
      const key = `${item.latitude},${item.longitude}`;
      //if the item doesn't have lat and long set the key to a blank array
      if (!grouped.has(key)) grouped.set(key, []);
      //The item is then pushed to the group map
      grouped.get(key).push(item);
    });

    //Start geometry logic
    const geometries = [];
    pointsRef.current = [];
    //Loop through the grouped map's entries to create each of the geometry objects
    for (const [key, entries] of grouped.entries()) {
      //Use the callback variable for the length of the map
      const count = entries.length;

      //base stats for each dimension of the geometries
      const baseSize = 0.03;      // width along tangent
      const minHeight = 0.03;     // base radial length
      const heightFactor = 0.015; // extra length per overlapping point
      const maxHeight = 0.3;      // cap height

      // Cap the radial length for maximum height value
      const radialLength = Math.min(minHeight + (count - 1) * heightFactor, maxHeight);
      //default the latitude and longitude objects to the first entry in groups
      const { latitude, longitude } = entries[0];

      dataRef.current.push(entries[0]);             //Push one data item per geometry in the exact same order

      //create x,y, and z values from the returned output coordinate array and correct x,y, and z coordinate placement with transformationHackUtility
      
      const json = convertObjectsToMultiPointGeoJSON("Congestion", [entries[0]]);
      const sphereCoords = convertGeoJSONToSphereCoordinates(json, radius);
      const rawPoint = sphereCoords.output_coordinate_array[0];
      const [x, y, z] = tranformationHackUtility([rawPoint])[0];

      //push new pointrefs to the variable
      pointsRef.current.push([x, y, z]);

      // Create box geometry with radialLength calculated earlier
      const geometry = new BoxGeometry(baseSize, 0.03, radialLength);

      // Compute radial vector
      const len = Math.hypot(x, y, z) || 1;
      const dx = x / len;
      const dy = y / len;
      const dz = z / len;

      // Translate along radial direction so base sits on sphere
      const translationMatrix = new Matrix4().makeTranslation(
        x + dx * radialLength / 2,
        y + dy * radialLength / 2,
        z + dz * radialLength / 2
      );

      // Rotate box to face outward
      const tempObject = new Object3D();
      tempObject.position.set(x, y, z);
      tempObject.lookAt(0, 0, 0);
      const lookAtMatrix = new Matrix4().makeRotationFromEuler(tempObject.rotation);

      const finalMatrix = new Matrix4().multiplyMatrices(translationMatrix, lookAtMatrix);

      geometry.applyMatrix4(finalMatrix);
      geometries.push(geometry);
    }

    console.log("Geometries:", geometries);

    // Merge all BoxGeometries into a single mesh
    try {
      if (geometries.length > 0) {
        return BufferGeometryUtils.mergeGeometries(geometries, true);
      }
    } catch (e) {
      console.error("Failed to merge heatmap geometries.", e);
    }

    return geometries.length > 0
      ? BufferGeometryUtils.mergeGeometries(geometries, true)
      : null;

  }, [data, radius]);


  useEffect(() => {
    if (groupRef.current) {
    }
  }, [])



  const material = new MeshBasicMaterial({ color: 0xff00ff });        //default to box geometry if image fails to load

  //start new code for point links$
  // Map a raycast faceIndex to the original box index using geometry groups
  function faceToPointIndex(geom, faceIndex) {

    // faceIndex is a triangle index; groups are in index units, so multiply by 3
    const triStart = faceIndex * 3
    const groups = geom.groups || []
    for (let i = 0; i < groups.length; i++) {
      const g = groups[i]

      // group.start/count are in index units
      if (triStart >= g.start && triStart < g.start + g.count) return i
    }
    return null
  }

  function handlePointerMove(e) {
    e.stopPropagation()

    // e.object is the merged mesh; e.faceIndex tells us which triangle
    const geom = e.object.geometry
    const idx = faceToPointIndex(geom, e.faceIndex ?? 0)
    if (idx == null || !pointsRef.current[idx]) {
      setHoverIdx(null)
      setHoverPos(null)
      document.body.style.cursor = 'auto'
      return
    }
    const p = pointsRef.current[idx]

    // nudge the tooltip outward a hair so it doesn't clip into the globe
    const offset = 0.12
    setHoverIdx(idx)
    setHoverPos([p[0], p[1] + offset, p[2]])
    document.body.style.cursor = dataRef.current[idx]?.url ? 'pointer' : 'auto'
  }

  function handlePointerOut() {
    setHoverIdx(null)
    setHoverPos(null)
    document.body.style.cursor = 'auto'
  }

  function handleClick(e) {
    e.stopPropagation();
    console.log(e.target)

    const geom = e.object.geometry;
    const idx = faceToPointIndex(geom, e.faceIndex ?? 0);

    if (idx == null) {
      // Clicked empty space → remove popup
      setSelectedGroup(null);
      return;
    }

    const clicked = dataRef.current[idx];
    if (!clicked) return;

    // Find all articles that share the same lat/lon, from the full list
    const group = allDataRef.current.filter(
      item =>
        item.latitude === clicked.latitude &&
        item.longitude === clicked.longitude
    );

    setSelectedGroup(group);
  }



  //Put the link functionality onto the 3D rendering once the geometries have been merged
  return mergedGeometry ? (
    <>
      <mesh
        ref={groupRef}
        //material={material}
        onPointerMove={handlePointerMove}
        onPointerOut={handlePointerOut}
        onClick={handleClick}
        onPointerMissed={() => setSelectedGroup(null)}
      >
        <primitive object={mergedGeometry} attach="geometry" />

        {/* Insertion of texture in replacement of box geometry */}
        <meshBasicMaterial
          map={texture}
          transparent={true}
          depthWrite={false}
          side={2}
          alphaTest={0.5}
        />

      </mesh>

      {selectedGroup && (
        <Html>
          <div 
          className='news-congestion-link'
          onWheel={(e) => e.stopPropagation()}
          >
            {selectedGroup.map((article, i) => (
              <div key={i} style={{ marginBottom: "12px" }}>
                <div style={{ fontWeight: "bold" }}>{article.title}</div>
                <div style={{ color: "white" }}>
                  {article.city}, {article.country}
                </div>
                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ color: "#4A78FF", fontSize: "0.85rem" }}
                >
                  Read Article
                </a>
              </div>
            ))}
          </div>
        </Html>
      )}

    </>
  ) : null;
}

export default NewsPopulate;
