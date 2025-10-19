import Flights from 'src/components/builders/Flights';
import Disasters from 'src/components/builders/Disasters';
import Weather from 'src/components/builders/Weather';
import Precipitation from 'src/components/builders/Precipitation';
import Shaders from 'src/components/builders/Shaders';
import NewsCongestion from 'src/components/builders/NewsCongestion';

function UpdateFilter({ activeFilter }) {
  const showShaders = !['Temperature', 'Precipitation'].includes(activeFilter);

  return (
    <>
      {showShaders && <Shaders />}
      <group>
        <Flights radius={2} visible={activeFilter === 'Flights'} />
        <Disasters radius={2} visible={activeFilter === 'Disasters'} />
        <NewsCongestion radius={2} visible={activeFilter === 'News'} />
        <Weather radius={2} visible={activeFilter === 'Temperature'} />
        <Precipitation radius={2} visible={activeFilter === 'Precipitation'} />
      </group>
      
    </>
  );
}


export default UpdateFilter;
