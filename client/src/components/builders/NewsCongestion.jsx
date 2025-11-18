import { useEffect, useState, useRef, useMemo } from 'react';
import {
  TextureLoader,
  Matrix4,
  BoxGeometry,
  Object3D,
  MeshBasicMaterial,
} from 'three';
import * as BufferGeometryUtils from 'three/examples/jsm/utils/BufferGeometryUtils.js';
import convertObjectsToMultiPointGeoJSON from 'src/utils/convertObjectsToMultiPointGeoJSON';
import convertGeoJSONToSphereCoordinates from 'src/utils/convertGeoJSONToSphereCoordinates';
import Error from 'src/components/builders/Error';
import api_conn from 'src/utils/api';
import ArticleList from './ArticleList'; // your popup component

function NewsPopulate({ radius, visible }) {
  const [data, setData] = useState(null);

  // Fetch data
  useEffect(() => {
    async function fetchData() {
      await api_conn
        .get('/api/NewsCongestion')
        .then((response) => response.data)
        .then((data) => {
          console.log(data);
          setData(data);
        })
        .catch((error) => console.error('Error fetching json file:', error));
    }

    fetchData();
  }, [radius]);

  if (!visible) return null;
  if (data && data.length === 0) return <Error />;

  return <>{data ? <BuildHeatmap data={data} radius={radius} /> : null}</>;
}

function BuildHeatmap({ data, radius }) {
  const groupRef = useRef();

  // Hover/click tracking
  const [hoverIdx, setHoverIdx] = useState(null);
  const pointsRef = useRef([]);
  const dataRef = useRef([]);

  // NEW: stores articles grouped per geometry
  const articlesGroupedRef = useRef([]);

  // Popup states
  const [clickedIdx, setClickedIdx] = useState(null);
  const [showPopup, setShowPopup] = useState(false);

  const texture = new TextureLoader().load('/images/ArticlePoint.jpg');

  const mergedGeometry = useMemo(() => {
    if (!data || !Array.isArray(data)) return null;

    const flatData = data.flat();
    dataRef.current = flatData;

    // Group by lat,long
    const grouped = new Map();
    flatData.forEach((item) => {
      const key = `${item.latitude},${item.longitude}`;
      if (!grouped.has(key)) grouped.set(key, []);
      grouped.get(key).push(item);
    });

    const geometries = [];
    pointsRef.current = [];
    articlesGroupedRef.current = []; // reset

    for (const [key, entries] of grouped.entries()) {
      const count = entries.length;

      const baseSize = 0.03;
      const minHeight = 0.03;
      const heightFactor = 0.015;
      const maxHeight = 0.3;

      const radialLength = Math.min(
        minHeight + (count - 1) * heightFactor,
        maxHeight
      );

      const { latitude, longitude } = entries[0];
      const [x, y, z] = convertGeoJSONToSphereCoordinates(
        convertObjectsToMultiPointGeoJSON('Congestion', [entries[0]]),
        radius
      ).output_coordinate_array[0];

      pointsRef.current.push([x, y, z]);
      articlesGroupedRef.current.push(entries); // <— store the article list for this point

      const geometry = new BoxGeometry(baseSize, 0.03, radialLength);

      const len = Math.hypot(x, y, z) || 1;
      const dx = x / len,
        dy = y / len,
        dz = z / len;

      const translationMatrix = new Matrix4().makeTranslation(
        x + (dx * radialLength) / 2,
        y + (dy * radialLength) / 2,
        z + (dz * radialLength) / 2
      );

      const tempObject = new Object3D();
      tempObject.position.set(x, y, z);
      tempObject.lookAt(0, 0, 0);
      const lookAtMatrix = new Matrix4().makeRotationFromEuler(
        tempObject.rotation
      );

      const finalMatrix = new Matrix4().multiplyMatrices(
        translationMatrix,
        lookAtMatrix
      );

      geometry.applyMatrix4(finalMatrix);
      geometries.push(geometry);
    }

    try {
      return BufferGeometryUtils.mergeGeometries(geometries, true);
    } catch (e) {
      console.error('Failed to merge heatmap geometries.', e);
    }

    return null;
  }, [data, radius]);

  useEffect(() => {
    if (groupRef.current) {
      groupRef.current.rotation.x = -Math.PI * 0.5;
    }
  }, []);

  const material = new MeshBasicMaterial({ color: 0xff00ff });

  function faceToPointIndex(geom, faceIndex) {
    const triStart = faceIndex * 3;
    const groups = geom.groups || [];
    for (let i = 0; i < groups.length; i++) {
      const g = groups[i];
      if (triStart >= g.start && triStart < g.start + g.count) return i;
    }
    return null;
  }

  function handlePointerMove(e) {
    e.stopPropagation();

    const geom = e.object.geometry;
    const idx = faceToPointIndex(geom, e.faceIndex ?? 0);
    if (idx == null) {
      setHoverIdx(null);
      document.body.style.cursor = 'auto';
      return;
    }

    setHoverIdx(idx);
    document.body.style.cursor = 'pointer';
  }

  function handlePointerOut() {
    setHoverIdx(null);
    document.body.style.cursor = 'auto';
  }

  // NEW CLICK → open popup, not external link
  function handleClick(e) {
    e.stopPropagation();

    const geom = e.object.geometry;
    const idx = faceToPointIndex(geom, e.faceIndex ?? 0);

    if (idx == null) return;

    setClickedIdx(idx);
    setShowPopup(true);
  }

  return mergedGeometry ? (
    <>
      <mesh
        ref={groupRef}
        onPointerMove={handlePointerMove}
        onPointerOut={handlePointerOut}
        onClick={handleClick}
      >
        <primitive object={mergedGeometry} attach="geometry" />
        <meshBasicMaterial
          map={texture}
          transparent={true}
          depthWrite={false}
          side={2}
          alphaTest={0.5}
        />
      </mesh>

      {/* === YOUR NEW REACT POPUP === */}
      {showPopup && clickedIdx != null && (
        <ArticleList articles={articlesGroupedRef.current[clickedIdx]} />
      )}
    </>
  ) : null;
}

export default NewsPopulate;
