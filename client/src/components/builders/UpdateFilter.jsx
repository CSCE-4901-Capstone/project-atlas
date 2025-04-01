import Flights from 'src/components/builders/Flights';

function UpdateFilter({ activeFilter }) {
  switch (activeFilter) {
      case 'Flights':
        return <Flights radius={2} />;
      default:
        return null
  }
};

export default UpdateFilter;
