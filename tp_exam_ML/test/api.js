import axios from 'axios';

// Configuration de base pour axios
const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

export const getPredictions = async (context) => {
  try {
    const response = await api.post('/predict', { context });
    return response.data;
  } catch (error) {
    console.error("Erreur API:", error);
    throw error;
  }
};

export const checkHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};