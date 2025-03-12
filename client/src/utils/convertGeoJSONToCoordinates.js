function convertGeoJSONToSphereCoordinates(json, radius) {
  let geometries = parseGeometries(json);

  let output_coordinate_array = [];
  let coordinate_type = "";

  for (let i = 0; i < geometries.length; i++) {
    switch (geometries[i].type) {
      case "Point": {
        coordinate_type = "Point";
        let sphere_coordinates = convertToSphereCoordinates(geometries[i].coordinates, radius);
        output_coordinate_array.push(sphere_coordinates);
        break;
      }
      case "MultiPoint": {
        coordinate_type = "MultiPoint";
        for (let j = 0; j < geometries[i].coordinates.length; j++) {
          let sphere_coordinates = convertToSphereCoordinates(geometries[i].coordinates[j], radius);
          output_coordinate_array.push(sphere_coordinates);
        }
        break;
      }
      case "LineString": {
        coordinate_type = "LineString";
        let adjusted_input_coordinate_array = adjustCoordinateArray(geometries[i].coordinates);
        for (let j = 0; j < adjusted_input_coordinate_array.length; j++) {
          let sphere_coordinates = convertToSphereCoordinates(adjusted_input_coordinate_array[j], radius);
          output_coordinate_array.push(sphere_coordinates);
        }
        break;
      }
        
      case "Polygon":
        coordinate_type = "Polygon"
      case "MultiLineString": {
        if (!coordinate_type) {
          coordinate_type = "MultiLineString";
        }

        for (let j = 0; j < geometries[i].coordinates.length; j++) {

          let adjusted_input_coordinate_array = adjustCoordinateArray(geometries[i].coordinates[j]);
          for (let k = 0; k < adjusted_input_coordinate_array.length; k++) {
            let sphere_coordinates = convertToSphereCoordinates(adjusted_input_coordinate_array[k], radius);
            output_coordinate_array.push(sphere_coordinates);
          }
        }
        break;
      }
      case "MultiPolygon": {
        for (let j = 0; j < geometries[i].coordinates.length; j++) {
          for (let k = 0; k < geometries[i].coordinates[j].length; k++) {

            let adjusted_input_coordinate_array = adjustCoordinateArray(geometries[i].coordinates[j][k]);

            for (let l = 0; l < adjusted_input_coordinate_array.length; l++) {
              let sphere_coordinates = convertToSphereCoordinates(adjusted_input_coordinate_array[l], radius);
              output_coordinate_array.push(sphere_coordinates);
            }
          }
        }
        break;
      }
      default:
        throw new SyntaxError("GeoJSON format is invalid");
    } // end switch
  }

  return { coordinate_type, output_coordinate_array };
}

function parseGeometries(json) {
  let geometryArray = [];

  switch (json.type) {
    case "Feature":
      geometryArray.push(json.geometry);
      break;
    case "FeatureCollection":
      for (let i = 0; i < json.features.length; i++) {
        geometryArray.push(json.features[i].geometry);
      }
      break;
    case "GeometryCollection":
      for (let i = 0; i < json.geometries.length; i++) {
        geometryArray.push(json.geometries[i]);
      }
      break;
    default:
      throw new SyntaxError("GeoJSON format is invalid");
  }

  return geometryArray;
}

function convertToSphereCoordinates(input_coordinates, radius) {
  const lon = input_coordinates[0];
  const lat = input_coordinates[1];

  let x = Math.cos(lat * Math.PI / 180) * Math.cos(lon * Math.PI / 180) * radius;
  let y = Math.cos(lat * Math.PI / 180) * Math.sin(lon * Math.PI / 180) * radius;
  let z = Math.sin(lat * Math.PI / 180) * radius;

  return [x, y, z];
}

function adjustCoordinateArray(input_coordinate_array) {
  let adjusted_coordinate_array = [];
  for (let i = 1; i < input_coordinate_array.length; i++) {
    let point1 = input_coordinate_array[i - 1];
    let point2 = input_coordinate_array[i];

    adjusted_coordinate_array.push(point1);
    if (needsInterpolation(point1, point2)) {
      let interpolated_coordinate_array = [];
      interpolate(interpolated_coordinate_array, point1, point2);
      adjusted_coordinate_array.push(...interpolated_coordinate_array);
    }

    if (i === input_coordinate_array.length - 1) {
      adjusted_coordinate_array.push(point2);
    }
  }
  return adjusted_coordinate_array;
}

function needsInterpolation(point1, point2) {
  let [lon1, lat1] = point1;
  let [lon2, lat2] = point2;

  return Math.abs(lon2 - lon1) > 5 || Math.abs(lat2 - lat1) > 5;
}

function interpolate(interpolated_coordinate_array, point1, point2) {
  if (!needsInterpolation(point1, point2)) {
    return;
  }

  let mid = getMidpoint(point1, point2);

  interpolate(interpolated_coordinate_array, point1, mid);
  interpolated_coordinate_array.push(mid);
  interpolate(interpolated_coordinate_array, mid, point2);
}

function getMidpoint(point1, point2) {
  let lon = (point1[0] + point2[0]) / 2;
  let lat = (point1[1] + point2[1]) / 2;
  return [lon, lat];
}

export default convertGeoJSONToSphereCoordinates;
