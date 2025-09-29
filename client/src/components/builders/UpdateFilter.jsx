import Flights from 'src/components/builders/Flights';
import Weather from 'src/components/builders/Weather';
import Shaders from 'src/components/builders/Shaders';
import NewsCongestion from 'src/components/builders/NewsCongestion';

function UpdateFilter({ activeFilter }) {
  let showShaders = true;
  let filter = null;

  switch (activeFilter) {
      case 'Flights':
        filter = <Flights radius={2} />;
        break;
      case 'News':
        filter = <NewsCongestion radius={2} />;
        break;
      case 'Weather':
        showShaders = false
        filter = <Weather radius={2} layerType="Weather" />;
        break;
      case 'Precipitation': 
        showShaders = false
        filter = <Weather radius={2} layerType="Precipitation" />;
        break;
      default:
        filter = null;
  }

  return (
    <>
      { showShaders && <Shaders /> }
      { filter }
    </>
  )
};

export default UpdateFilter;
