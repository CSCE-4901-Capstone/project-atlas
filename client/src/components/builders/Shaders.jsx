import { useRef, useMemo } from 'react'
import { useThree } from '@react-three/fiber'
import { useFrame, useLoader } from '@react-three/fiber';
import * as THREE from 'three'
import gsap from 'gsap'

import convertGeoJSONToSphereCoordinates from "src/utils/convertGeoJSONToSphereCoordinates";
import * as turf from '@turf/turf'

function Shaders() {
  const cloudsRef = useRef();
 // Loads the earth texture
  const [map, alphaMap] = useLoader(THREE.TextureLoader, [
    "/images/clouds.jpg",
    "/images/05_earthcloudmaptrans.jpg",
  ]);

  const fresnelMat = useMemo(() => getFresnelMat(), []);

  useFrame(() => {
    if (cloudsRef.current) {
      cloudsRef.current.rotation.y += 0.00015;
    }
  })

  return (
    <>
      <mesh ref={cloudsRef}>
        <sphereGeometry args={[2.02, 51, 32]} />
        <meshPhongMaterial
          map={map}
          opacity={0.3}
          depthWrite={false}
          transparent={true}
          blending={THREE.AdditiveBlending}
          alphaMap={alphaMap}
        />
      </mesh>
      <mesh>
        <sphereGeometry args={[2.01, 51, 32]} />
        <primitive object={fresnelMat} attach="material" />
      </mesh>
    </>
  )
}

function getFresnelMat({rimHex = 0x0088ff, facingHex = 0x000000} = {}) {
  const uniforms = {
    color1: { value: new THREE.Color(rimHex) },
    color2: { value: new THREE.Color(facingHex) },
    fresnelBias: { value: 0.1 },
    fresnelScale: { value: 1.0 },
    fresnelPower: { value: 4.0 },
  };

  const vs = `
  uniform float fresnelBias;
  uniform float fresnelScale;
  uniform float fresnelPower;

  varying float vReflectionFactor;

  void main() {
    vec4 mvPosition = modelViewMatrix * vec4( position, 1.0 );
    vec4 worldPosition = modelMatrix * vec4( position, 1.0 );

    vec3 worldNormal = normalize( mat3( modelMatrix[0].xyz, modelMatrix[1].xyz, modelMatrix[2].xyz ) * normal );

    vec3 I = worldPosition.xyz - cameraPosition;

    vReflectionFactor = fresnelBias + fresnelScale * pow( 1.0 + dot( normalize( I ), worldNormal ), fresnelPower );

    gl_Position = projectionMatrix * mvPosition;
  }
  `;

  const fs = `
  uniform vec3 color1;
  uniform vec3 color2;

  varying float vReflectionFactor;

  void main() {
    float f = clamp( vReflectionFactor, 0.0, 1.0 );
    gl_FragColor = vec4(mix(color2, color1, vec3(f)), f);
  }
  `;

  const fresnelMaterial = new THREE.ShaderMaterial({
    uniforms: uniforms,
    vertexShader: vs,
    fragmentShader: fs,
    depthWrite: false,
    transparent: true,
    blending: THREE.AdditiveBlending,
  });
  return fresnelMaterial;
}

export default Shaders; 

