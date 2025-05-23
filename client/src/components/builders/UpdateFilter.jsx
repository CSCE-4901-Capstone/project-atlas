import Flights from 'src/components/builders/Flights';
import Weather from 'src/components/builders/Weather';

function UpdateFilter({ activeFilter }) {
  switch (activeFilter) {
      case 'Flights':
        return <Flights radius={2} />;
      case 'Weather':
        return <Weather radius={2} />;
      default:
        return null
  }
};

export default UpdateFilter;
