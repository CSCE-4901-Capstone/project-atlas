import { useEffect } from 'react'
import { useThree } from '@react-three/fiber'
import * as THREE from 'three'
import gsap from 'gsap'

import convertGeoJSONToSphereCoordinates from "src/utils/convertGeoJSONToSphereCoordinates";
import * as turf from '@turf/turf'

function CameraController({ selectedCountry, setClickDisabled}) {
  const { camera } = useThree()

  useEffect(() => {
    if (!selectedCountry) return

    fetch(`/json/outlines/${selectedCountry}.geojson`)
      .then(res => res.json())
      .then(json => {
        const countryFeature = json.features[0]
        const centerPoint = extractLargestPolygonCenterPoint(countryFeature);
        //const centerPoint = turf.center(countryFeature)
        const sphereCoordinates = convertGeoJSONToSphereCoordinates(centerPoint, 2.0)
        const targetPos = new THREE.Vector3(...sphereCoordinates.output_coordinate_array[0])

        const offsetPos = targetPos.clone().normalize().multiplyScalar(targetPos.length() + 3)

        const rotated = rotateAroundPoint(
          offsetPos,
          new THREE.Vector3(0, 0, 0),
          new THREE.Vector3(1, 0, 0),
          -Math.PI * 0.5
        )

        setClickDisabled(true)

        gsap.to(camera.position, {
          x: rotated.x,
          y: rotated.y,
          z: rotated.z,
          duration: 1,      
          ease: "power2.inOut",
          onUpdate: () => {
            camera.lookAt(targetPos)
          },
          onComplete: () => {
            setClickDisabled(false);
          }
        })

      })
      .catch(err => console.error(err))
  }, [selectedCountry, camera])

  return null
}

function extractLargestPolygonCenterPoint(feature) {
  // Step 1: split multipolygon into individual polygons
  const polys = turf.flatten(feature) // gives a FeatureCollection of polygons

  // Step 2: find largest polygon
  let largest = null
  let maxArea = -Infinity

  for (const feature of polys.features) {
    const area = turf.area(feature)
    if (area > maxArea) {
      maxArea = area
      largest = feature
    }
  }

  // Step 3: get the center of the largest polygon
  return turf.center(largest)  // or turf.centroid(largest)


}

function rotateAroundPoint(point, anchor, axis, angle) {
  const v = point.clone().sub(anchor)
  v.applyAxisAngle(axis, angle)
  v.add(anchor)
  return v
}

export default CameraController

