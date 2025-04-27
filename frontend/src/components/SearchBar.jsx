import { useState } from 'react';
import { getRecommendations, getGeminiResponse } from '../services/api';

const SearchBar = ({ onRecommendationsLoaded }) => {
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [geminiResult, setGeminiResult] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setGeminiResult(''); // Clear previous Gemini results

    try {
      // Check if the input is a customer ID (e.g., starts with "C")
      if (/^C\d+$/.test(inputValue)) {
        // Fetch recommendations for the customer
        const recommendations = await getRecommendations(inputValue, 5);
        onRecommendationsLoaded(recommendations);
      } else {
        // Use Gemini API for general queries
        const geminiResponse = await getGeminiResponse(inputValue);
        setGeminiResult(geminiResponse);
      }
    } catch (err) {
      setError('Failed to fetch results. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="search-form">
      <input
        type="text"
        placeholder="Enter Customer ID (e.g., C3805) or Query"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Loading...' : 'Submit'}
      </button>
      {error && <p className="error-message">{error}</p>}
      {geminiResult && (
        <div className="gemini-response">
          <h3>Gemini Response:</h3>
          <p>{geminiResult}</p>
        </div>
      )}
    </form>
  );
};

export default SearchBar;
