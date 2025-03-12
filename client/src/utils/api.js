import axios from 'axios'

const api_conn = axios.create({
  baseURL: import.meta.env.VITE_API_URL
});


export default api_conn;
