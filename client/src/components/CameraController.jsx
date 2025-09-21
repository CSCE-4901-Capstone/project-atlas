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
        const centerPoint = turf.center(countryFeature)
        const cartesian = convertGeoJSONToSphereCoordinates(centerPoint, 2.0)
        const targetPos = new THREE.Vector3(...cartesian.output_coordinate_array[0])

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

function rotateAroundPoint(point, anchor, axis, angle) {
  const v = point.clone().sub(anchor)
  v.applyAxisAngle(axis, angle)
  v.add(anchor)
  return v
}

export default CameraController

