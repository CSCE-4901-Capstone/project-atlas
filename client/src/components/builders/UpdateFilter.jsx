import Flights from 'src/components/builders/Flights';
import Weather from 'src/components/builders/Weather';
import NewsCongestion from 'src/components/builders/NewsCongestion';

function UpdateFilter({ activeFilter }) {

  switch (activeFilter) {
      case 'Flights':
        return <Flights radius={2} />;
      case 'Temperature':
        return <Weather radius={2} layerType="Temperature" />;
      case 'Precipitation': 
        return <Weather radius={2} layerType="Precipitation" />;
      case 'News':           //filter used for News Congestion Heatmap
          return  <NewsCongestion radius={2} />;
      default:
        return null;
  }
};

export default UpdateFilter;
