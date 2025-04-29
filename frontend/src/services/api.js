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

// Updated function for Gemini API integration
export const getGeminiResponse = async (prompt) => {
  try {
    const apiKey = import.meta.env.VITE_GEMINI_API_KEY; // Access environment variable
    console.log("API Key:", apiKey); // For debugging only, remove in production

    const response = await axios.post(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`,
      {
        contents: [{ parts: [{ text: prompt }] }],
      },
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    return response.data.candidates[0].content.parts[0].text;
  } catch (error) {
    console.error('Gemini API Error:', error);
    throw error;
  }
};

// Add this function if it's not already in your api.js file
export const generateInsightsForRecommendations = async (recommendations) => {
  if (!recommendations || recommendations.length === 0) {
    return null;
  }

  // Create a summary of the recommendations
  const categories = [...new Set(recommendations.map(r => r.Category))];
  const brands = [...new Set(recommendations.map(r => r.Brand))];
  const priceRange = {
    min: Math.min(...recommendations.map(r => r.Price)),
    max: Math.max(...recommendations.map(r => r.Price))
  };

  const prompt = `Based on these product recommendations in categories: ${categories.join(', ')}
  from brands: ${brands.join(', ')} with price range $${priceRange.min} - $${priceRange.max},
  provide a brief 1-2 sentence insight about these recommendations. Make it sound helpful for a shopper.`;

  try {
    return await getGeminiResponse(prompt);
  } catch (error) {
    console.error('Error generating insights:', error);
    return '';
  }
};
