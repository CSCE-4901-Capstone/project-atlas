import { Matrix4, Vector3 } from 'three';

// Used to fix some issues with aligning the 3d space and incoming data
function transformationHackUtility(coords, matrix) {
  console.log(coords)
  const rotationMatrix = matrix || new Matrix4().makeRotationX(-Math.PI * 0.5);

  return coords.map(([x, y, z]) => {
    const v = new Vector3(x, y, z).applyMatrix4(rotationMatrix);
    return [v.x, v.y, v.z];
  });
}

export default transformationHackUtility;
