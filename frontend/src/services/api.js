import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Update with your backend URL

export const getRecommendations = async (customerId, topN = 5) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/recommend/${customerId}`, {
      params: { top_n: topN },
    });
    return response.data.recommendations;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
    throw error;
  }
};