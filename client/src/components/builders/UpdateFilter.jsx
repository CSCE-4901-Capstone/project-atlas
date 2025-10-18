import Flights from 'src/components/builders/Flights';
import Disasters from 'src/components/builders/Disasters';
import Weather from 'src/components/builders/Weather';
import Precipitation from 'src/components/builders/Precipitation';
import Shaders from 'src/components/builders/Shaders';
import NewsCongestion from 'src/components/builders/NewsCongestion';

function UpdateFilter({ activeFilter }) {
  let showShaders = true;
  let filter = null;

  switch (activeFilter) {
      case 'Flights':
        filter = <Flights radius={2} />;
        break;
      case 'Disasters':
        filter = <Disasters radius={2} />;
        break;
      case 'News':
        filter = <NewsCongestion radius={2} />;
        break;
      case 'Temperature':
        showShaders = false
        filter = <Weather radius={2} />; 
        break;
      case 'Precipitation': 
        showShaders = false
        filter = <Precipitation radius={2} />;
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
