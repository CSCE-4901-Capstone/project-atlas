function convertObjectsToMultiPointGeoJSON(type, objects) {
  let points = []

  switch(type) {
    case 'Flights':
      for (const object of objects) {
        if (object.longitude && object.latitude) {
          points.push([object.longitude, object.latitude]) ;
        }
      }
      break;
  }

  return {
      "type": "Feature",
      "properties": {
      },
      "geometry": {
        "type": "MultiPoint",
        "coordinates": points
      }
  }
}

export default convertObjectsToMultiPointGeoJSON;
