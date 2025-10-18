import CountryOutline from 'src/components/builders/CountryOutline'

function CountryHighlight({ selectedCountry }) {

  return (
    <>
      {selectedCountry ? <CountryOutline filename={`${selectedCountry}.geojson`} radius={2.001} color={'rgb(255,255,255)'}/> : null}
      <CountryOutline filename='all.geojson' radius={2} color={'rgb(10,10,10)'}/>
    </>
  )
}

export default CountryHighlight;
