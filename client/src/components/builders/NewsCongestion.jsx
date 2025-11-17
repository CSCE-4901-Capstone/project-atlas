import { useEffect, useState, useRef, useMemo } from 'react';
import { TextureLoader, Matrix4, BoxGeometry, Object3D, PlaneGeometry, MeshBasicMaterial, Mesh } from 'three';
import * as BufferGeometryUtils from 'three/examples/jsm/utils/BufferGeometryUtils.js';
import convertObjectsToMultiPointGeoJSON from 'src/utils/convertObjectsToMultiPointGeoJSON';
import convertGeoJSONToSphereCoordinates from 'src/utils/convertGeoJSONToSphereCoordinates';
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
function sizeIncrease() {

}

function BuildHeatmap({ data, radius }) {
  const groupRef = useRef();

  //Reference parameters for the hover and click
  const [hoverIdx, setHoverIdx] = useState(null)   // which point is hovered
  const [hoverPos, setHoverPos] = useState(null)   // world position for tooltip
  const pointsRef = useRef([])                     // stores [x,y,z] for each point
  const dataRef = useRef([])                       // stores original data aligned to points
  //end

  /*//Referecne parameters for the rising box geometry
  // rising animation state
    const posAttrRef = useRef(null)       // geometry.attributes.position
    const basePosRef = useRef(null)       // Float32Array copy of original positions
    const indexRef = useRef(null)         // geometry.index.array
    const riseMetaRef = useRef([])        // [{start,count, dx,dy,dz, t, delay}]
    const allDoneRef = useRef(false)
    const RISE_HEIGHT = 0.2               // how far to rise outward (tweak)
    const RISE_SPEED = 1.0                // seconds to reach full height (tweak)
    //end*/

  const texture = new TextureLoader().load('/images/ArticlePoint.jpg');       //populate the image for a news Point on the globe

  const mergedGeometry = useMemo(() => {
  if (!data || !Array.isArray(data)) return null;

  console.log("Incoming data:", data);

  // --- Normalize data to 1D ---
  const flatData = data.length > 0 && Array.isArray(data[0])
    ? data.flat()      // handles 2D
    : data;            // already 1D

  console.log("Flattened data:", flatData);

  // Store reference to original data
  dataRef.current = flatData;

  // --- Group points by latitude + longitude ---
  const grouped = new Map();
  flatData.forEach(item => {
    const key = `${item.latitude},${item.longitude}`;
    if (!grouped.has(key)) grouped.set(key, []);
    grouped.get(key).push(item);
  });

  const geometries = [];
pointsRef.current = [];

for (const [key, entries] of grouped.entries()) {
  const count = entries.length;

  const baseSize = 0.03;        // width along tangent
  const minHeight = 0.03;       // base radial length
  const heightFactor = 0.015;   // extra length per overlap
  const radialLength = minHeight + (count - 1) * heightFactor;

  const { latitude, longitude } = entries[0];

  const [x, y, z] = convertGeoJSONToSphereCoordinates(
    convertObjectsToMultiPointGeoJSON("Congestion", [entries[0]]),
    radius
  ).output_coordinate_array[0];

  pointsRef.current.push([x, y, z]);

  // Step 1: Create a flat BoxGeometry (height along Z initially)
  const geometry = new BoxGeometry(baseSize, 0.03, radialLength);

  // Step 2: Compute the radial vector (direction away from globe center)
  const len = Math.hypot(x, y, z) || 1;
  const dx = x / len;
  const dy = y / len;
  const dz = z / len;

  // Step 3: Translate the box along radial vector by half its height so base sits on sphere
  const translationMatrix = new Matrix4().makeTranslation(
    x + dx * radialLength / 2,
    y + dy * radialLength / 2,
    z + dz * radialLength / 2
  );

  // Step 4: Rotate box to face outward (away from globe center)
  const tempObj = new Object3D();
  tempObj.position.set(x, y, z);
  tempObj.lookAt(0, 0, 0);
  const lookAtMatrix = new Matrix4().makeRotationFromEuler(tempObj.rotation);

  const finalMatrix = new Matrix4()
    .multiplyMatrices(translationMatrix, lookAtMatrix);

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
      groupRef.current.rotation.x = -Math.PI * 0.5; // Quick hack to fix rotation
    }
  }, [])

  /*// Use effect prepares rising animation when BoxGeometry becomes available
  useEffect(() => {
    const mesh = groupRef.current
    if (!mesh || !mesh.geometry) return
    const geom = mesh.geometry

    // cache attributes needed
    posAttrRef.current = geom.attributes.position
    indexRef.current   = geom.index?.array || null
    if (!posAttrRef.current) return

    // store base positions once
    if (!basePosRef.current || basePosRef.current.length !== posAttrRef.current.array.length) {
      basePosRef.current = new Float32Array(posAttrRef.current.array) // clone
    }

    // build one entry per group (each original box)
    const groups = geom.groups || []
    const pts = pointsRef.current || []
    riseMetaRef.current = groups.map((g, i) => {
      
      // outward direction = normalized point position
      const p = pts[i] || [0,0,1]
      const len = Math.hypot(p[0], p[1], p[2]) || 1
      const dx = p[0] / len, dy = p[1] / len, dz = p[2] / len
      return {
        start: g.start,         // index buffer range (triangles)
        count: g.count,
        dx, dy, dz,
        t: 0,                   // progress 0..1
        delay: (i % 50) * 0.02, // subtle stagger; tweak or set 0
      }
    })
    allDoneRef.current = false
  }, [mergedGeometry])*/

  /*//UseFrame used for animating every frame of the BoxGeometry
  useFrame((_, delta) => {
  if (allDoneRef.current) return
  const posAttr = posAttrRef.current
  const base = basePosRef.current
  const idxArr = indexRef.current
  const meta = riseMetaRef.current
  if (!posAttr || !base || !meta?.length) return

  // ease function (smooth finish)
  const easeOutCubic = (x) => 1 - Math.pow(1 - x, 3)

  let allDone = true
  for (let m of meta) {
    // handle per-item delay
    if (m.delay > 0) { m.delay -= delta; allDone = false; continue }
    if (m.t < 1) { m.t = Math.min(1, m.t + delta / RISE_SPEED); allDone = false }
    const h = RISE_HEIGHT * easeOutCubic(m.t)

    if (idxArr) {
      // indexed geometry: move only vertices referenced by this group's index range
      const end = m.start + m.count
      for (let k = m.start; k < end; k++) {
        const vi = idxArr[k] * 3
        posAttr.array[vi    ] = base[vi    ] + m.dx * h
        posAttr.array[vi + 1] = base[vi + 1] + m.dy * h
        posAttr.array[vi + 2] = base[vi + 2] + m.dz * h
      }
    } else {
      // non-indexed (unlikely after merge), fallback by vertex range
      const startV = m.start * 1 // triangle index == vertex index here
      const endV = startV + m.count
      for (let vi = startV * 3; vi < endV * 3; vi += 3) {
        posAttr.array[vi    ] = base[vi    ] + m.dx * h
        posAttr.array[vi + 1] = base[vi + 1] + m.dy * h
        posAttr.array[vi + 2] = base[vi + 2] + m.dz * h
      }
    }
  }
  posAttr.needsUpdate = true
  allDoneRef.current = allDone
  })*/


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
    e.stopPropagation()
    const geom = e.object.geometry
    const idx = faceToPointIndex(geom, e.faceIndex ?? 0)
    if (idx == null) return
    const url = dataRef.current[idx]?.url
    if (url) window.open(url, '_blank', 'noopener,noreferrer')
  }
  //end of new code for points

  //Put the link functionality onto the 3D rendering once the geometries have been merged
  return mergedGeometry ? (
    <>
      <mesh
        ref={groupRef}
        //material={material}
        onPointerMove={handlePointerMove}
        onPointerOut={handlePointerOut}
        onClick={handleClick}
      //raycast={(...args) => Mesh.prototype.raycast.apply(args[0].object, args.slice(1))} // keep default
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
      {hoverIdx != null && hoverPos && dataRef.current[hoverIdx]?.url && (
        <Html>
          <a
            href={dataRef.current[hoverIdx].url}
            target="_blank"
            rel="noopener noreferrer"
            onPointerDown={(e) => e.stopPropagation()}       // ensure that we can still drag the globe
            className='news-congestion-link'
          >
            {dataRef.current[hoverIdx]?.title || 'Open article'}
          </a>
        </Html>
      )}
    </>
  ) : null;
  //end of new code
}

export default NewsPopulate;
