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
    case 'Congestion':      //do the same thing as done for flights filter by getting longitude and latitude points
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
