import Flights from 'src/components/builders/Flights';
import Disasters from 'src/components/builders/Disasters';
import Weather from 'src/components/builders/Weather';
import Precipitation from 'src/components/builders/Precipitation';
import Shaders from 'src/components/builders/Shaders';
import NewsCongestion from 'src/components/builders/NewsCongestion';

function UpdateFilter({ activeFilter }) {
  const showShaders = !['Temperature', 'Precipitation'].includes(activeFilter);
  let filter;

  switch (activeFilter) {
      case 'Temperature':
        filter = <Weather radius={2} />; 
        break;
      case 'Precipitation': 
        filter = <Precipitation radius={2} />;
        break;
      default:
        filter = null;
  }

  return (
    <>
      {showShaders && <Shaders />}
      <group>
        <Flights radius={2} visible={activeFilter === 'Flights'} />
        <Disasters radius={2} visible={activeFilter === 'Disasters'} />
        <NewsCongestion radius={2} visible={activeFilter === 'News'} />
      </group>

      {filter}
      
    </>
  );
}


export default UpdateFilter;
