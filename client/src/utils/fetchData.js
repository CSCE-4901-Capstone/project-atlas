import { cache } from 'react';
import api_conn from 'src/utils/api';

const fetchData = cache(async (link) => {
  try {
    const response = await api_conn.get(link);
    return response.data;
  } catch (error) {
    console.error('Error fetching json file:', error);
    return null;
  }
});

export default fetchData;

