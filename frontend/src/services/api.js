import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Backend URL for recommendations

// Existing function for fetching recommendations
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

// New function for Gemini API integration
export const getGeminiResponse = async (prompt) => {
  try {
    const apiKey = import.meta.env.VITE_GEMINI_API_KEY; // Access environment variable
    const response = await axios.post(
      'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent', // Replace with actual endpoint
      {
        contents: [{ parts: [{ text: prompt }] }],
      },
      {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data.candidates[0].content.parts[0].text; // Extract response text
  } catch (error) {
    console.error('Gemini API Error:', error);
    throw error;
  }
};
