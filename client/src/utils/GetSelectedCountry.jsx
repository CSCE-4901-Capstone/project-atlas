import * as turf from '@turf/turf';

async function getSelectedCountry(point) {
  try {
    // Fetch the countries json
    const response = await fetch(`/json/countries.json`);
    const countries_json = await response.json();

    // Convert the 3D point to geographic coordinates
    let convertedPoint = convertToGeographicCoordinates(point);

    // Find the selected country
    return findSelectedCountry(countries_json, convertedPoint);
  } catch (error) {
    console.error('Error loading GeoJSON file:', error);
    return null;
  }
}

// Converts input x, y, z coordinates into longitude and latitude
function convertToGeographicCoordinates(input_coordinates) {
  let x = input_coordinates.x;
  let y = input_coordinates.y;
  let z = input_coordinates.z;

  // Rotates values to fix sphere orientation
  let rotatedY = -z;
  let rotatedZ = y;

  // Convert to Longitude 
  let lon = Math.atan2(rotatedY, x);

  // Convert to Latitude
  let r = Math.sqrt(x * x + rotatedY * rotatedY + rotatedZ * rotatedZ);
  let lat = Math.asin(rotatedZ / r);

  // Convert to degrees
  let lonDeg = lon * (180 / Math.PI);
  let latDeg = lat * (180 / Math.PI);

  return [lonDeg, latDeg];
}

// Find which country was selected
function findSelectedCountry(json, point) {
  // Pulls the features and turf point
  let features = json['features'];
  let turfPoint = turf.point(point);

  for (const feature of features) {
    let geometry = feature['geometry'];

    if (geometry.type === "Polygon") {
      let polygon = turf.polygon(geometry.coordinates);
      if (turf.booleanPointInPolygon(turfPoint, polygon)) {
        return feature.properties.name; // Return the country name
      }
    } 
    else if (geometry.type === "MultiPolygon") {
      let multiPolygon = turf.multiPolygon(geometry.coordinates);
      if (turf.booleanPointInPolygon(turfPoint, multiPolygon)) {
        return feature.properties.name;
      }
    }
  }

  return null;
}

export default getSelectedCountry;

