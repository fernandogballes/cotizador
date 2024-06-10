import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

export const fetchOffers = async () => {
  try {
    const response = await axios.get(`${API_URL}/ofertas_disponibles/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching offers:', error);
    throw error;
  }
};
