// src/components/SearchBar.jsx
import { useState } from 'react';
import { getRecommendations, getGeminiResponse } from '../services/api';
import './SearchBar.css';

const SearchBar = ({ onRecommendationsLoaded, onInsightsLoaded, onLoadingStateChange }) => {
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    onLoadingStateChange(true);

    try {
      // Check if the input is a customer ID (e.g., starts with "C")
      if (/^C\d+$/.test(inputValue)) {
        // Fetch recommendations for the customer
        const recommendations = await getRecommendations(inputValue, 5);
        onRecommendationsLoaded(recommendations);

        // Generate insights about the recommendations
        if (recommendations && recommendations.length > 0) {
          const insights = await generateInsightsForRecommendations(recommendations);
          onInsightsLoaded(insights);
        } else {
          onInsightsLoaded('');
        }
      } else {
        // Use Gemini API for product queries
        const prompt = `Generate 4 product recommendations for "${inputValue}" in e-commerce.
        For each product include: Product_ID (like P12345), Category, Subcategory,
        Price (numeric value between 20-200), Brand, Ratings (1-5), and Recommendation_Score (80-100).
        Also include a brief 1-2 sentence Description field for each product.
        Format the response as a valid JSON array with no markdown formatting or backticks.
        The response should be ONLY the raw JSON array, nothing else.`;

        const geminiResponse = await getGeminiResponse(prompt);

        try {
          // Extract JSON from the response by removing markdown formatting
          let jsonStr = geminiResponse;

          // Remove markdown code blocks if present
          if (jsonStr.includes("```")) {
            jsonStr = jsonStr.replace(/```json\s*/g, '').replace(/```\s*/g, '');
          }

          // Trim whitespace
          jsonStr = jsonStr.trim();

          // Parse the JSON
          const productRecommendations = JSON.parse(jsonStr);
          onRecommendationsLoaded(productRecommendations);
          onInsightsLoaded(`Top recommendations for "${inputValue}" based on product popularity, features, and reviews.`);
        } catch (parseError) {
          console.error('Failed to parse Gemini response as JSON:', parseError);
          console.log('Raw response:', geminiResponse);
          setError('Failed to process product recommendations. Please try another query.');
          onRecommendationsLoaded([]);
          onInsightsLoaded('');
        }
      }
    } catch (err) {
      setError('Failed to fetch results. Please try again.');
      console.error('Error:', err);
      onRecommendationsLoaded([]);
      onInsightsLoaded('');
    } finally {
      setLoading(false);
      onLoadingStateChange(false);
    }
  };

  return (
    <div className="search-container">
      <form onSubmit={handleSubmit} className="search-form">
        <input
          type="text"
          placeholder="Search for products or enter customer ID (e.g., C3805)"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          className="search-input"
          required
        />
        <button type="submit" disabled={loading} className="search-button">
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      {error && <p className="error-message">{error}</p>}
    </div>
  );
};

export default SearchBar;
